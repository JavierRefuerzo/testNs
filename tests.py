#!/usr/bin/env python3
"""
Polyglot v3 node server OpenSprinkler
Copyright (C) 2021 Javier Refuerzo

"""



from iTachLib.controller.codeSetParser import CodeSetParser
from iTachLib.tests.codeSet import CodeSet


codeSet = CodeSet()

data = codeSet.getCodeSet()
# data = codeSet.getParmSet()

parser = CodeSetParser()

parser.parse(data)
#StationTests(creds)