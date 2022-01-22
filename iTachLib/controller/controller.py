#!/usr/bin/env python3
"""
Polyglot v3 node server iTach IR
Copyright (C) 2021 Javier Refuerzo

"""

#import udi_interface
from typing import Callable, List
from objects.errors import Errors
from nodes.controller.drivers import ErrorValues
from iTachLib.controller.Device import Device
import socket

LOGGER = udi_interface.LOGGER


class Controller :
    errors: Errors = None
    errorObserver: Callable = None
    #TODO: Add removal listener

    address: str
    deviceList: List[Device]


    def __init__(self, address: str, errorObserver: Callable):
        self.address = address
        self.address = self.address.replace("http://", "")
        self.deviceList = []
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


    # ------ Setters

    # should be called after all data is parsed into a List of Devices
    def updateDevices(self, devices: List[Device]):
        LOGGER.info("update Devices")
        # update the device list to ensure the device is listed
        # there may be multiple items for the same device in device list
        # so do NOT just replace the values
        for newDevice in devices:
            device = self._getDevice(newDevice)
            if device != None:
                LOGGER.info("update existing Device: " + device.name)
                #the device exists so update values
                device.updateButtons(newIrCodeList=newDevice.buttons)
            else:
                LOGGER.info("Adding New Device: " + newDevice.name)
                # the device does not exist so add to list
                self.deviceList.append(newDevice)
       
        # all values should now be updated, so remove any that are not in the list
        self._cleanDeviceList(newDeviceList=devices)


    #removes any device not in new device list
    def _cleanDeviceList(self, newDeviceList: List[Device]):
        LOGGER.info("clean Device List")
        # check if the device already exists
        removalList: List[Device] = []
        for oldDevice in self.deviceList:
            exists = False
            for newDevice in newDeviceList:
                if oldDevice.name == newDevice.name:
                    exists = True
                    break
            if not exists:
                removalList.append(oldDevice)

        #remove devices
        for device in removalList:
            LOGGER.info("removing Device: " + device.name)
            # notify observes of removal
            device.willRemoveDevice()
            self.deviceList.remove(device)


    def _getDevice(self, newDevice: Device) -> Device:
        LOGGER.info("Get Device")
        # check if the device already exists
        for oldDevice in self.deviceList:
            if newDevice.name == oldDevice.name:
                LOGGER.info("Device Found: " + oldDevice.name)
                return oldDevice
        #the device does not exist
        LOGGER.info("device not found")
        return None
    
    # ---- Command functions

    def send_command(self, command) -> any:
        byte_size=4096
        timeout=10
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        command = command + "\r"
        response: any = None
        try:
            sock.connect((self.address, 4998))
            command = command.encode()
            sock.sendall(command)
            response = self.format_message(sock.recv(byte_size))
            print("Sent: " + str(command))
            print("Received: " + response)
            LOGGER.info("RECEIVED: " + response)
        except socket.error as error:
            print(repr(error))
            LOGGER.info("ERROR: " + str(error))
            response = "ERROR: " + str(error)
        finally:
            sock.close()
            LOGGER.info("Close Socket")
            return response

      
    
    def format_message(self, msg):
        """format message"""
        if isinstance(msg, bytes):
            return msg.decode()
        return msg

     # ---- Get update

    