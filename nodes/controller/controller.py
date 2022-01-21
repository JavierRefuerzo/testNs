#!/usr/bin/env python3
"""
Polyglot v3 node server OpenSprinkler
Copyright (C) 2021 Javier Refuerzo

"""
from os import name
import udi_interface
from typing import Callable, List, final
from iTachLib.controller.Device import Device
from iTachLib.controller.codeSetParser import CodeSetParser
from nodes.controller.drivers import Drivers
from nodes.controller.drivers import StatusValues
from nodes.controller.drivers import ErrorValues
from nodes.device.DeviceNode import DeviceNode
from objects.errors import Errors
from iTachLib.controller.controller import Controller as ITach
from nodes.observers.polyglotObserver import PolyglotObserver
from constants.params import Params

LOGGER = udi_interface.LOGGER
Custom = udi_interface.Custom



'''
Controller 
'''
class Controller(udi_interface.Node):
    # Node Definitions
    id = 'ctl'
    address='iTach_IR' 
    name='iTach IR'

    # Status Drivers
    drivers = [
            {'driver': Drivers.status.value, 'value': StatusValues.true.value, 'uom': 2},
            ]
    

    # Data
    iTach: ITach = None
    deviceNodeList: List[DeviceNode]
    errorCode: int = ErrorValues.none.value

    # Nodes/Node Holders


    #shared observer
    polyObserver: PolyglotObserver

    
    def __init__(self, polyglot):
        super(Controller, self).__init__(polyglot, self.address, self.address, self.name)   
        
        self.poly = polyglot
        self.polyObserver = PolyglotObserver(self.poly)
        self.deviceNodeList = []

        #set custom params
        self.Parameters = Custom(polyglot, 'customparams')

        #Set initaial status 
        #self.deviceList = []
        self.setStatus(statusEnum=StatusValues.true)

        # start processing events and create or add our controller node
        self.poly.ready()
        
        # Add this node to ISY
        self.poly.addNode(self)


        # subscribe to the events we want
        self.setMqttObsevers()
        self.observeShared()

        #this should be moved out of this class and into an observer model
        #test_connect = connect.Connect(self.poly, controller=self)




    #---------- Status Setters

    def setStatus(self, statusEnum: StatusValues):
        self.setDriver(Drivers.status.value, statusEnum.value, True, True)

    def setError(self, error: Errors):
        #only update error code if it has changed
        if self.errorCode == error.code:
            return
        LOGGER.info('setError: ' + error.text)
        self.errorCode = error.code
        self.setDriver(Drivers.error.value, error.code, True, True)
        # set/remove notices
        if self.errorCode == ErrorValues.none.value:
            self.poly.Notices.clear()
        elif self.errorCode == ErrorValues.firmware.value:
            self.poly.Notices['firmware'] = 'OpenSprinkler Firmware Update Required to use this Node Server. Minimum firmware supported is 2.1.9. Please be sure to backup open sprinkler before upgrading firmware as you settings will be removed! https://openthings.freshdesk.com/support/home see User Manuals and select your hardware 3.x or 2.x'



    #---------- Shared Observer
    def observeShared(self):
        self.polyObserver.stop.attach(self.stop)
        self.polyObserver.customParams.attach(self.parameterHandler)
        self.polyObserver.polls.attach(self.poll)



    #---------- MQTT Observers

    def setMqttObsevers(self):
        self.poly.subscribe(self.poly.START, self.start, self.address)
        #other mqtt subsribe functions in shared observer
    
    def stop(self):
        LOGGER.info(' stop')
        self.setStatus(statusEnum=StatusValues.false)
        self.poly.stop()

    def start(self):
        LOGGER.info(' start called')
        self.poly.setCustomParamsDoc()
        self.poly.updateProfile()

    def parameterHandler(self, params):
        self.Parameters.load(params)
        LOGGER.info('GET Custom params TEST ' + str(self.Parameters))
        self.processParameters(params=params)

    def poll(self, polltype):
        if 'shortPoll' in polltype:
            print("shortPoll")
        # if 'longPoll' in polltype:
        #     self.updateStatus()


    #---------- Command  Observers

    

    #Set Command Observers
    commands = {}


   
#---------- Business Logic

    def processParameters(self, params):
        LOGGER.info('Process Params: ' + str(len(params)))
        # make sure defined params are set
        self.processDefinedParams(params)
        
        #clear the device list
        deviceList: List[Device] = []

        # process ir codes for each param
        for param in params:
            LOGGER.info('Process Param: ' + param)
            # det not try to parse defined param
            enum = Params.get(value=param)
            if enum != None:
                LOGGER.info('Defined Param: ' + param)
                continue

            # This is a button code
            LOGGER.info('Device Param: ' + param)
            device = self.getDevice(params, param)
            if device == None:
                LOGGER.info('Could not get Device: ' + param)
                continue
            deviceList.append(device)

        #check that the controller is not null
        if self.iTach == None:
            LOGGER.info('iTach Controller NOT set: ')
            return

        # update the iTach Controller with new device list
        self.iTach.updateDevices(device=deviceList)
        # update device nodes
        self.updateDeviceList()

            
    def processDefinedParams(self, params):
        #get url
        url = params[Params.url.value]
        if self.iTach == None:
            LOGGER.info('Creating iTach Controller')
            self.iTach = ITach(address=url, errorObserver=self.setError)
        else:
            LOGGER.info('Updating iTach URL')
            self.iTach.address = url


    def getDevice(self, params, param) -> Device :
        try:
            parser = CodeSetParser(params[param])
            codeSet = parser.codeSet
            if len(codeSet) == 0:
                LOGGER.info("Parse Error: code list is empty")
                return None
            LOGGER.info('Number of ir codes for "'+ param  + '": ' + str(len(parser.codeSet)))
            return Device(name=param, buttons=codeSet)
        except Exception as e:
            LOGGER.info("Parse Error: " + str(e))
            return None

        

    def updateDeviceList(self):
        if self.iTach == None:
            return
        # get the device list from iTach
        devices = self.iTach.deviceList
        for device in devices:
            exists = False
            for node in self.deviceNodeList:
                if node.name == device.name:
                    #node exists update the device i.e. ir codes
                    node.device = device
                    exists = True
                    break

            if not exists:
                #create new node
                deviceNode = DeviceNode(self.poly, self.address, )
                self.deviceNodeList.append(deviceNode)

        # All DeviceNodes should be added/updated
        # Remove any nodes which no longer exist
        self._cleanDeviceList(newDeviceList=devices)

        #TODO Create NodeDef, NLS, etc

    #removes any device not in new device list
    def _cleanDeviceList(self, newDeviceList: List[Device]):
        # check if the device already exists
        removalList: List[DeviceNode] = []
        for oldDevice in self.deviceNodeList:
            exists = False
            for newDevice in newDeviceList:
                if oldDevice.device.name == newDevice.name:
                    exists = True
                    break
            if not exists:
                removalList.append(oldDevice)
                
        #remove devices
        for device in removalList:
            # TODO: remove device from ISY
            LOGGER.info("TODO remove device: " + device.device.name)
            self.deviceNodeList.remove(device)