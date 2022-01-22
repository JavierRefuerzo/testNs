#!/usr/bin/env python3
"""
Polyglot v3 node server OpenSprinkler
Copyright (C) 2021 Javier Refuerzo

"""



from typing import List
from iTachLib.controller.irCode import IrCode
from iTachLib.controller.controller import Controller as ITACH


#codeSet = CodeSet()

# data = codeSet.getCodeSet()
#THIS MAY NOT WORK WITH UDI LOGGING ENABLED IN PARSER
#data = codeSet.getParmSet()

#parser = CodeSetParser()

#parser.parse(data)
#StationTests(creds)

print("Started")

irCode1 = IrCode("POWER TOGGLE", "sendir,0:1,1,38000,1,69,339,170,21,21,21,63,21,21,21,21,21,63,21,21,21,63,21,63,21,63,21,21,21,63,21,63,21,21,21,63,21,63,21,21,21,21,21,21,21,63,21,21,21,21,21,21,21,21,21,21,21,63,21,63,21,21,21,63,21,63,21,63,21,63,21,63,21,1466,339,84,21,3633")
irCode2 = IrCode("Test Button2", "sendir,1:1,1,38000,1,69,339,170,21,21,21,63,21,21,21,21,21,63,21,21,21,63,21,63,21,63,21,21,21,63,21,63,21,21,21,63,21,63,21,21,21,63,21,21,21,63,21,63,21,63,21,21,21,63,21,21,21,21,21,63,21,21,21,21,21,21,21,63,21,21,21,63,21,1466,339,84,21,3633")

command = irCode1.command(buttonCode=1, connector=1, repeat=1)
iTach = ITACH(address="http://192.168.1.70", errorObserver=None)
response = iTach.send_command(command=command)

if response != None:
    print("Command: " + response)
else:
    print("No response" )

# irList: List[IrCode] = []
# irList.append(irCode1)
# irList.append(irCode2)

# device1 = Device("device One", irList)
# device2 = Device("device Two", irList)

# deviceList: List[Device] = []
# deviceList.append(device1)
# deviceList.append(device2)

# mod = DocumentModifier()
# mod.writeFiles(deviceList)


print("Finished")