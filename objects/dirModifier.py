#!/usr/bin/env python3
"""
Polyglot v3 node server OpenSprinkler
Copyright (C) 2021 Javier Refuerzo

"""


from curses import nl
import os
from typing import List
import re
from constants.NodeDefTemplate import NodeDefTemplate

from constants.defaultNLS import DefaultNls
from iTachLib.controller.Device import Device


class DirModifier :
    
    devices: List[Device]

    def __init__(self, devices: List[Device]):
        print("init ")
        self.devices = devices
        self.makeNls()
        self.makeNodeDef()

    def makeNls(self):
        print("makeNls ")
        # There is only one nls, so read the nls template and write the new one
        en_us_txt = "profile/nls/en_us.txt"
        self.make_file_dir(en_us_txt)
        nls = open(en_us_txt,  "w")
        nls.write(DefaultNls.nls)
        for index, device in enumerate(self.devices):
            print("device: " + device.name)
            nls.write("#Device - " + device.name + "\n")    
            print("num of codes: " + str(len(device.buttons)))
            for code in device.buttons:
                #This should be changed to nodeAddress
                name = self._getAddress(device)
                command = name + "-" + str(index) + "\n"
                nls.write(command)    
            # add double line between commands
            nls.write("\n\n")

        nls.close()

    def makeNodeDef(self):
        nodeDef_xml = "profile/nodedef/devices.xml"
        self.make_file_dir(nodeDef_xml)
        nodeDef = open(nodeDef_xml,  "w")
        template = NodeDefTemplate()

        nodeDef.write(template.prifix)
        for index, device in enumerate(self.devices):
            length = len(device.buttons) - 1
            name = self._getAddress(device)
            nodeXml = template.getNodeDef(name, length)
            print("device: " + device.name)
            nodeDef.write('  <!-- Device ' + device.name + "-->")    
            nodeDef.write(nodeXml)    

        nodeDef.write(template.suffix)
        nodeDef.close()

    def make_file_dir(self, file_path):
        directory = os.path.dirname(file_path)
        if not os.path.exists(directory):
            os.makedirs(directory)
        return True

    def _getAddress(self, device: Device) -> str:
        name = device.name
        name = name.replace(" ", "_")
        name = name.lower()
        name = self._get_valid_node_name(name)
        return name

    def _get_valid_node_name(self, name, max_length=14) -> str:
        offset = max_length * -1
        # Only allow utf-8 characters
        #  https://stackoverflow.com/questions/26541968/delete-every-non-utf-8-symbols-froms-string
        name = bytes(name, 'utf-8').decode('utf-8','ignore')
        # Remove <>`~!@#$%^&*(){}[]?/\;:"'` characters from name
        sname = re.sub(r"[<>`~!@#$%^&*(){}[\]?/\\;:\"']+", "", name)
        # And return last part of name of over max_length
        return sname[offset:].lower()