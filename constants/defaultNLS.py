#!/usr/bin/env python3
"""
Polyglot v3 node server OpenSprinkler
Copyright (C) 2021 Javier Refuerzo

"""





class DefaultNls() :

    nls = '''
#Controller
ND-ctl-NAME = iTach IR
ND-ctl-ICON = Output

ST-ctl-ST-NAME = NodeServer Online
#ST-ctl-GV0-NAME = Last Error Message

#irdevice
NDN-irdevice-NAME = IR Code Set
NDN-irdevice-ICON = Output
ST-irdevice-ST-NAME = Last Status

#Shared command names

CMD-STOP-NAME = Stop IR
CMD-COMMAND-NAME = Send IR
CMDP-BUTTON-NAME = Button Name
CMDP-CODE-NAME = Alternate Codes
CMDP-CONNECTOR-NAME = Connector
CMDP-REPETE-NAME = Repeat


ERRORS-0 = None
ERRORS-1 = Missing Password
ERRORS-2 = Missing IP Address
ERRORS-3 = Connection Error
ERRORS-4 = CheckLogs
ERRORS-5 = Invalid URL
ERRORS-6 = OpenSprinkler Firmware Update Required (min 2.1.9)


CODE-1 = Button Code 1
CODE-2 = Button Code 2

CONNECTOR-1 = Left 1
CONNECTOR-2 = Center 2
CONNECTOR-3 = Right 3
    
'''

