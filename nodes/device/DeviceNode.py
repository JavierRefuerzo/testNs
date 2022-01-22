#!/usr/bin/env python3
"""
Polyglot v3 node server OpenSprinkler
Copyright (C) 2021 Javier Refuerzo
MIT License
"""


from enum import Enum
import udi_interface
from iTachLib.controller.Device import Device
from nodes.controller.drivers import ErrorValues
from objects.DocumentModifier import DocumentModifier
from objects.polyglotObserver import PolyglotObserver



LOGGER = udi_interface.LOGGER
Custom = udi_interface.Custom


#enum for drivers
class Drivers(Enum):
    errorDriver = "GV0"



'''
This is our Zone device node. 
'''
class DeviceNode(udi_interface.Node):
    #------------- Node Definitions
    id = "irdevice"

    #------------- Status Drivers
    # Status Drivers
    drivers = [
            {'driver': Drivers.errorDriver.value, 'value': ErrorValues.none.value, 'uom': 2}
            ]

    
    #------------- Data
    device: Device


    #shared observer
    polyObserver: PolyglotObserver


    def __init__(self, polyglot, parentAddress: str, device: Device, polyObserver: PolyglotObserver):
        LOGGER.info(' init, parent: ')
        self.poly = polyglot
        self.device = device
        self.polyObserver = polyObserver
        self.polyObserver.iTachError.attach(self.setError)

        #Set initial values
        
        #change the station name to include stationId
        mod = DocumentModifier()
        self.address = mod.getAddress(device)
        self.id = self.address
        self.name = mod.get_valid_node_name(device.name)

        # Add global observer
        

        # Add this node to ISY
        super(DeviceNode, self).__init__(polyglot, parentAddress, self.address, self.name)
        self.poly.addNode(self)

        LOGGER.info('update station status')
        self.setDriver(Drivers.errorDriver.value, ErrorValues.none.value, True, True)
        # subscribe to the events we want
        


    #---------- Unique Node Properties

   
    
    #---------- Status Setters
   
    def setError(self, error: int):
        self.setDriver(Drivers.errorDriver.value, error, True, True)
    
   
    #---------- MQTT Observers

    


    #---------- Command  Observers


    #  <p id="BUTTON" editor="button" />
    #  <p id="CODE" editor="code" />
    #  <p id="CONNECTOR" editor="connector" />
    #  <p id="REPETE" editor="repete" />
    def cmdCOMMAND(self, command):
        query = command.get('query')
        button_uom25 = int(query.get('BUTTON.uom25'))
        code_uom25 = int(query.get('CODE.uom25'))
        connector_uom25 = int(query.get('CONNECTOR.uom25'))
        repeat_uom56 = int(query.get('REPEAT.uom56'))
        button = self.device.getIrCode(index=button_uom25)
        if button == None:
            return
        data = button.command(buttonCode=code_uom25, connector=connector_uom25, repeat=repeat_uom56)    
        response = self.polyObserver.send_command(command=data)
        LOGGER.info('response: ' + str(response))

    # <p id="CONNECTOR" editor="connector" />
    def cmdSTOP(self, command):
        query = command.get('query')
        connector_uom25 = int(query.get('CONNECTOR.uom25'))
        response = self.polyObserver.send_stop_ir_command(connector_uom25)
        LOGGER.info('restponse: ' + str(response))


   
    
    commands = {
        "COMMAND":cmdCOMMAND, 
        'STOP': cmdSTOP,
    }

    #---------- Business Logic
        
  

   
  

    

    
   
            

    



