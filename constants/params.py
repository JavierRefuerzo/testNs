#!/usr/bin/env python3
"""
Polyglot v3 node server OpenSprinkler
Copyright (C) 2021 Javier Refuerzo

"""


from enum import Enum
from typing import List


class Params(Enum) :
    #These values are also hard coded into server.json
    url = "url"

    
    def get(value: str):
        list: List[str] = []
        for enum in Params:
            if enum.value == value:
                return enum
        return None   




    
    