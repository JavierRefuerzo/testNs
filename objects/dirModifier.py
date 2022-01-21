#!/usr/bin/env python3
"""
Polyglot v3 node server OpenSprinkler
Copyright (C) 2021 Javier Refuerzo

"""


from curses import nl
import os
from typing import List

from constants.defaultNLS import DefaultNls
from iTachLib.controller.Device import Device


class DirModifier :
    
    devices: List[Device]

    def __init__(self, devices: List[Device]):
        self.devices = devices
        self.makeNls()

    def makeNls(self):
        # There is only one nls, so read the nls template and write the new one
        en_us_txt = "profile/nls/en_test.txt"
        self.make_file_dir(en_us_txt)
        nls = open(en_us_txt,  "w")
        nls.write(DefaultNls.nls)
        for index, device in enumerate(self.devices):
            nls.write("#Device - " + device.name + "\n")    
            for code in device.buttons:
                #This should be changed to nodeAddress
                name = self.get_valid_node_name(device.name)
                command = name + "-" + str(index) + "\n"
                nls.write(command)    
            # add double line between commands
            nls.write("\n\n")

        nls.close()


    def make_file_dir(self, file_path):
        directory = os.path.dirname(file_path)
        if not os.path.exists(directory):
            os.makedirs(directory)
        return True

    def get_valid_node_name(self, name, max_length=14) -> str:
        offset = max_length * -1
        # Only allow utf-8 characters
        #  https://stackoverflow.com/questions/26541968/delete-every-non-utf-8-symbols-froms-string
        name = bytes(name, 'utf-8').decode('utf-8','ignore')
        # Remove <>`~!@#$%^&*(){}[]?/\;:"'` characters from name
        sname = re.sub(r"[<>`~!@#$%^&*(){}[\]?/\\;:\"']+", "", name)
        # And return last part of name of over max_length
        return sname[offset:].lower()