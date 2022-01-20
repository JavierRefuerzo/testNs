#!/usr/bin/env python3
"""
Polyglot v3 node server OpenSprinkler
Copyright (C) 2021 Javier Refuerzo

"""
import json
import udi_interface
from typing import Callable, List, final
from iTachLib.controller.codeSetParser import CodeSetParser
from nodes.controller.drivers import Drivers
from nodes.controller.drivers import StatusValues
from nodes.controller.drivers import ErrorValues
from objects.errors import Errors
from iTachLib.controller.controller import Controller as OpenSprinkler
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
    address='opensprinkler' 
    name='OpenSprinkler'

    # Status Drivers
    drivers = [
            {'driver': Drivers.status.value, 'value': StatusValues.true.value, 'uom': 2},
            {'driver': Drivers.error.value, 'value': ErrorValues.none.value, 'uom': 25},
            {'driver': Drivers.controllerEnabled.value, 'value': StatusValues.false.value, 'uom': 2},
            {'driver': Drivers.rainDelay.value, 'value': StatusValues.false.value, 'uom': 2},
            {'driver': Drivers.sensor1.value, 'value': StatusValues.false.value, 'uom': 2},
            {'driver': Drivers.sensor2.value, 'value': StatusValues.false.value, 'uom': 2},
            {'driver': Drivers.runningProgram.value, 'value': 0, 'uom': 25},
            ]
    

    # Data
    openSprinkler: OpenSprinkler = None
    errorCode: int = ErrorValues.none.value
    customParamsHandlers: List[Callable] = []
    currentProgram: int = None

    # Nodes/Node Holders


    #shared observer
    polyObserver: PolyglotObserver

    
    def __init__(self, polyglot):
        super(Controller, self).__init__(polyglot, self.address, self.address, self.name)   
        
        self.poly = polyglot
        self.polyObserver = PolyglotObserver(self.poly)

        #set custom params
        self.Parameters = Custom(polyglot, 'customparams')

        #Set initaial status 
        self.setStatus(statusEnum=StatusValues.true)

        # start processing events and create or add our controller node
        self.poly.ready()
        
        # Add this node to ISY
        self.poly.addNode(self)

        #Create objects which hold child nodes


        # subscribe to the events we want
        self.setMqttObsevers()
        self.observeShared()

        #this should be moved out of this class and into an observer model
        #test_connect = connect.Connect(self.poly, controller=self)




    #---------- Status Setters

    def setStatus(self, statusEnum: StatusValues):
        self.setDriver(Drivers.status.value, statusEnum.value, True, True)

    def setControllerEnabled(self, value: int):
        self.setDriver(Drivers.controllerEnabled.value, value, True, True)

    def setRainDelayDriver(self, value: int):
        self.setDriver(Drivers.rainDelay.value, value, True, True)

    def setSensorOneDriver(self, value: int):
        self.setDriver(Drivers.sensor1.value, value, True, True)
    
    def setSensorTwoDriver(self, value: int):
        self.setDriver(Drivers.sensor2.value, value, True, True)

    def setRunningProgramDriver(self, value: List[List[int]]):
        final = 0
        for station in value:
            program = station[0]
            if program > final:
                final = program
        #only set the value if it has changed
        if self.currentProgram != None and self.currentProgram == final:
            return
        self.currentProgram = final
        self.setDriver(Drivers.runningProgram.value, final, True, True)

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
        self.getCodeSet(params=params)
        #self.polyObserver.updateCustomParam(params)

    def poll(self, polltype):
        if 'shortPoll' in polltype:
            print("shortPoll")
        # if 'longPoll' in polltype:
        #     self.updateStatus()


    #---------- Command  Observers

    

    #Set Command Observers
    commands = {
           
        }


   
#---------- Business Logic

    def getCodeSet(self, params):
        LOGGER.info('makeRequest')
        codes: CodeSetParser
        for param in params:
            LOGGER.info("Param is: " + str(param))
            #do not parse type params
            enum = Params.get(value=param)
            LOGGER.info("enum is: " + str(enum))
            if enum != None:
                LOGGER.info("Not parsing IR Param is: " + param)
                continue
            
            #LOGGER.info("Param is: " + str(param))
            LOGGER.info("Value is: " + params[param])
            try:
                codes = CodeSetParser()
                codes.parse(param)
            except Exception as e:
                LOGGER.info("Parse Error: " + str(e))
                continue

            if len(codes.codeset) == 0:
                LOGGER.info("Parse Error: code list is empty")
                continue
            
        LOGGER.info("Number of ir codes " + str(len(codes.codeSet)))
        print(len(codes.codeSet))

        

            

        
    def processParam(self, param):
        LOGGER.info("Param is: " + str(param))
        LOGGER.info("Value is: " + str(param.value))
        LOGGER.info("Key is: " + str(param.key))
        # try:
        #     codes = CodeSetParser().parse(param)
        # except Exception as e:
        #     LOGGER.info("Parse Error: " + str(e))

        # if len(codes.codeset) == 0:
        #     LOGGER.info("Parse Error: code list is empty")