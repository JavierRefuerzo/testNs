#!/usr/bin/env python3
"""
Polyglot v3 node server OpenSprinkler
Copyright (C) 2021 Javier Refuerzo

"""

import udi_interface
import iTachLib
from objects.LiveObject import LiveObject
from iTachLib.controller.controller import Controller as Itach

LOGGER = udi_interface.LOGGER





class PolyglotObserver :
    
    #polyglot
    poly = None

    #controller (repository)
    iTach: Itach = None

    # Observed objects
    customParams: LiveObject
    stop: LiveObject
    polls: LiveObject
    iTachError: LiveObject
    
    #customParamObserverList: List[Callable]
    
    
    def __init__(self, poly):
        self.poly = poly

        #------------set initial Data

        # observed objects
        self.customParams = LiveObject()
        self.stop = LiveObject()
        self.polls = LiveObject()
        self.iTachError = LiveObject()

        # observe mqtt
        self.setMqttObsevers()


        
    #---------- MQTT Observers

    def setMqttObsevers(self):
        self.poly.subscribe(self.poly.STOP, self.stop.update)
        self.poly.subscribe(self.poly.CUSTOMPARAMS, self.customParams.update)
        self.poly.subscribe(self.poly.POLL, self.polls.update)



    #---------- Getters

    def send_command(self, command):
        if self.iTach == None:
            return

        self.iTach.send_command(command= command)
        #TODO Check errors and update observers