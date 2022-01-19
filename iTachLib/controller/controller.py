#!/usr/bin/env python3
"""
Polyglot v3 node server OpenSprinkler
Copyright (C) 2021 Javier Refuerzo

"""
from tkinter.messagebox import NO
from typing import Callable
from objects.errors import Errors
from nodes.controller.drivers import ErrorValues




class Controller :
    errors: Errors = None
    errorObserver: Callable = None

    address: str

    def __init__(self, address: str, errorObserver: Callable):
        self.address = address
        # TODO Add connection Test

    # ------ Setters with update listeners

    def setErrors(self, error: Errors):
        #set error to global
        self.errors = error
        #return if there is no observer
        if self.errorObserver == None:
            return
        #update observer    
        self.errorObserver(self.errors)
    
    '''
    Use these functions to set/clear errors so they are passed to observer function
    '''
    def clearError(self):
        noneError = Errors("none", code=ErrorValues.none.value)
        self.setErrors(noneError)

    

    # ---- Command functions


   

     # ---- Get update

    