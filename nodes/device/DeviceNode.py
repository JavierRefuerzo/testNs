#!/usr/bin/env python3
"""
Polyglot v3 node server OpenSprinkler
Copyright (C) 2021 Javier Refuerzo
MIT License
"""

from enum import Enum
from typing import List
import udi_interface
from iTachLib.controller.Device import Device
from nodes.observers.polyglotObserver import PolyglotObserver



LOGGER = udi_interface.LOGGER
Custom = udi_interface.Custom


#enum for drivers
class Drivers(Enum):
    status = "ST"

#enum for status values
class StatusValues(Enum):
    false = 0
    true = 1


'''
This is our Zone device node. 
'''
class DeviceNode(udi_interface.Node):
    #------------- Node Definitions
    id = "irdevice"

    #------------- Status Drivers
    # Status Drivers
    drivers = [
            {'driver': Drivers.status.value, 'value': StatusValues.true.value, 'uom': 2}
            ]

    
    #------------- Data
    device: Device


    #shared observer
    polyObserver: PolyglotObserver


    def __init__(self, polyglot, parentAddress: str, device: Device, polyObserver:PolyglotObserver):
        LOGGER.info(' init, parent: ')
        self.poly = polyglot
        self.device = device

        #Set initial values
        
        #change the station name to include stationId
        self.address = self.setAddress(device=device)

        # Add global observer
        

        # Add this node to ISY
        super(DeviceNode, self).__init__(polyglot, self.address, self.address, device.name)
        self.poly.addNode(self)

        LOGGER.info('update station status')
        self.setDriver(Drivers.status.value, StatusValues.true.value, True, True)
        # subscribe to the events we want
        


    #---------- Unique Node Properties

    def setAddress(self, device: Device) -> str:
        LOGGER.info('set address')
        name = device.name
        name = name.replace(" ", "_")
        name = name.lower()
        address = 'device_' +  name
        return address
    
    #---------- Status Setters
   
    
   
    #---------- MQTT Observers

    


    #---------- Command  Observers


    #  <p id="BUTTON" editor="button" />
    #  <p id="CODE" editor="code" />
    #  <p id="CONNECTOR" editor="connector" />
    #  <p id="REPETE" editor="repete" />
    def cmdCOMMAND(self, command):
        LOGGER.info('cmd COMMAND')
        val = int(command.get('value'))
        if val == None:
            return
        

    # <p id="CONNECTOR" editor="connector" />
    def cmdSTOP(self, command):
        LOGGER.info('cmd STOP')


   
    
    commands = {
        "COMMAND":cmdCOMMAND, 
        'STOP': cmdSTOP,
    }

    #---------- Business Logic
        
  

   
  

    

    
   
            

    



