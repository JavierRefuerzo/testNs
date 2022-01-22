#!/usr/bin/env python3
"""
Polyglot v3 node server OpenSprinkler
Copyright (C) 2021 Javier Refuerzo

"""

from iTachLib.controller.IrCode import IrCode
from typing import List





class Device :

    name: str
    buttons: List[IrCode]

    def __init__(self, name: str, buttons: List[IrCode]):
        self.name = name
        self.buttons = buttons


    def updateButtons(self, newIrCodeList: List[IrCode]):
        for newIrCode in  newIrCodeList:
            # get the existing code from the list if exists
            irCode = self._getIrCode(newIrCode)
            # update buttons and button codes
            if irCode != None:
                #there is an existing code int the list, so update values
                irCode.gcCodeOne = newIrCode.gcCodeOne
                irCode.gdCodeTwo = newIrCode.gdCodeTwo
            else:
                 #there is no existing code add to the list
                irCode =  newIrCode
                self.buttons.append(irCode)
        # all buttons should now be updated
        #remove any buttons which do not exist
        self._cleanButtonList(newIrCodeList=newIrCodeList)

    # this should be called before device is removed from controller 
    # so any observers can remove the device from ISY
    def willRemoveDevice(self):
        if self.removedObserver != None:
            self.removedObserver()
            

    def _cleanButtonList(self, newIrCodeList: List[IrCode]):
        # check if the device already exists
        removalList: List[IrCode] = []
        for oldIrCode in self.buttons:
            exists = False
            for newCode in newIrCodeList:
                if oldIrCode.buttonName == newCode.buttonName:
                    exists = True
                    break
            if not exists:
                removalList.append(oldIrCode)

        #remove devices
        for code in removalList:
            self.buttons.remove(code)

    # gets the irCode from the list of buttons if it exists
    def _getIrCode(self, newCode: IrCode) -> IrCode:
        for button in self.buttons:
            #if the ir code arleady exists update values
            if newCode.buttonName == button.buttonName:
                button.gcCodeOne = newCode.gcCodeOne
                button.gdCodeTwo = newCode.gdCodeTwo
                return button
        return None

    def getIrCode(self, index: int) -> IrCode:
        if len(self.buttons) > index:
            return self.buttons[index]
        return None