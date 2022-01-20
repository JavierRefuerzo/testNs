#!/usr/bin/env python3
"""
Polyglot v3 node server OpenSprinkler
Copyright (C) 2021 Javier Refuerzo

"""



import ast
import email
import json
from typing import List

from iTachLib.controller.irCode import IrCode


class CodeSetParser:


    def __init__(self):
        print("CodeSetParser init")

    def parse(self, data: str):
        print ("parsing started")

        #This splits the ir codes from the email data
        email = data.split('''function, code1, hexcode1, code2, hexcode2''')

        
        #this removes the data names from the array
        if len(email) > 1 :
            data = email.pop(1)
        
        #strip any blank space or new lines
        data = data.strip()

        #split into codes
        #Note Plolyglot may set this as two blank spaces
        codes = data.split("\n\n")
    
        
        for index, code in enumerate(codes):
            code = code.strip()
            #check for empty strings
            if not code:
                print ("index Empty: " + str(index))
                continue
            
            #replace any blank items in the list as it will crash string literal comnversion
            code = code.replace(",,",",").replace(",,",",").replace(",,",",")

            #make code into a string literal list
            code = "[" + code + "]"

            #replace any empty strings at the end of the list i.e "XX","XX",]
            code = code.replace(",]","]")

            # codeInfo:List = ast.literal_eval(code)
            # size = len(codeInfo)

            print("codeInfo is:\n" + code + "\n")

            # for string in codeInfo:
            #     print(string)

            codeInfo = json.loads(code)
            size = len(codeInfo)

            # we need at least a function name
            if size < 2:
                print("code size too small")
                continue
            
            print("Code: " + str(index) + ". len: " + str(size))
            print("function: " + codeInfo[0])
            print("code1 " + codeInfo[1])

            ir = IrCode(button=codeInfo[0], gcCodeOne=codeInfo[1])
            # if size > 2:
            #     print("hexcode1 " + codeInfo[2])
            if size > 3:
                print("hexcode1 " + codeInfo[3])
                ir.gdCodeTwo = codeInfo[3]
            # if size > 4:
            #     print("hexcode2 " + codeInfo[4])
            
           
            #print("codeInfo is:\n" + codeInfo + "\n")

            #print("index" + str(index) + "\n: " + code + "\n")