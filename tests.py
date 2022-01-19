#!/usr/bin/env python3
"""
Polyglot v3 node server OpenSprinkler
Copyright (C) 2021 Javier Refuerzo

"""



from iTachLib.controller.credenital import Credential
from constants.params import Params
from iTachLib.tests.programTests import ProgramTests
from iTachLib.tests.stationTests import StationTests



params = {Params.password : "opendoor", Params.url: "http://192.168.1.5"}

creds = Credential(params=params)
if creds.errors != None:
    print("Couild not get CREDS: " + creds.errors.text)
    exit()


ProgramTests(creds)

#StationTests(creds)