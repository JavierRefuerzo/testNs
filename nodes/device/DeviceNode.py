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
from objects.DirModifier import DirModifier
from objects.polyglotObserver import PolyglotObserver



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
        mod = DirModifier()
        self.address = mod.getAddress(device)
        self.id = self.address
        self.name = mod.get_valid_node_name(device.name)

        # Add global observer
        

        # Add this node to ISY
        super(DeviceNode, self).__init__(polyglot, parentAddress, self.address, self.name)
        self.poly.addNode(self)

        LOGGER.info('update station status')
        self.setDriver(Drivers.status.value, StatusValues.true.value, True, True)
        # subscribe to the events we want
        


    #---------- Unique Node Properties

   
    
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
        
  

   
  

    

    
   
            

    



