#!/usr/bin/env python3
"""
Polyglot v3 node server OpenSprinkler
Copyright (C) 2021 Javier Refuerzo

"""



class IrCode :
    
   
    buttonName: str
    gcCodeOne: str
    gdCodeTwo: str 


    def __init__(self, button, gcCodeOne):
       self.buttonName = button
       self.gcCodeOne = gcCodeOne
       self.gdCodeTwo = None
       

    #sendir,1:1,1,38000,
    # setState,
    # 1 is module number (may change), staring with zero
    # :1 is connector

    def command(self, buttonCode: int, connector: int, repeat: int) -> str:
        
        # get button code
        code = self.gcCodeOne
        if buttonCode == 2 and self.gdCodeTwo != None:
            code = self.gdCodeTwo
        
        # split ir code for edit
        split = code.split(",")
        # set the connector
        orgConnector = split[1]
        connectorSplit = orgConnector.split(":")
        connector = connectorSplit[0] + ":" + str(connector)
        split[1] = connector
        # set repeat
        split[4] = str(repeat)

        command: str = ",".join(split)

        print(command)
        return command

    

        #sendir,1:1,1,38000,1,69,339,171,21,21,21,63,21,21,21,21,21,63,21,21,21,63,21,63,21,21,21,21,21,63,21,63,21,21,21,63,21,63,21,21,21,21,21,21,21,63,21,21,21,21,21,21,21,63,21,21,21,63,21,63,21,21,21,63,21,63,21,63,21,21,21,63,21,1509,339,84,21,3634



#class Commands :


    #get_NET see #5 in API
    #getdevices
    #getversion
    #get_SERIAL
    #set_SERIAL
    #setstate
    #get_IR we may need to query this for type
    #stopir
    #getstate
    #state

    #CHANNEL SELECT\",\"sendir, 1:1,                      1,                            38000,   1,              69,                  339,171,21,21,21,63,21,21,21,21,21,
    #                   sendir, connector addresss (1:2), ID (confirmation 0 - 65535), frequency,repete (max 50), offset (always odd),


    #stop

    # def __init__(self):
    #     print("init")
