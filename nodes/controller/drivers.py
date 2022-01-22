#!/usr/bin/env python3
"""
Polyglot v3 node server OpenSprinkler
Copyright (C) 2021 Javier Refuerzo

"""
from enum import Enum


#enum for drivers
class Drivers(Enum):
    status = "ST"

#enum for status values
class StatusValues(Enum):
    false = 0
    true = 1


class ErrorValues(Enum):
    connection = -1
    none = 0
    ERR_01 = 1
    ERR_02 = 2
    ERR_03 = 3
    ERR_04 = 4
    ERR_05 = 5
    ERR_06 = 6
    ERR_07 = 7
    ERR_08 = 8
    ERR_09 = 9
    ERR_10 = 10
    ERR_11 = 11
    ERR_12 = 12
    ERR_13 = 13
    ERR_14 = 14
    ERR_15 = 15
    ERR_16 = 16
    ERR_17 = 17
    ERR_18 = 18
    ERR_19 = 19
    ERR_20 = 20
    ERR_21 = 21
    ERR_22 = 22
    ERR_23 = 23
    ERR_24 = 24
    ERR_25 = 25
    ERR_26 = 26
    ERR_27 = 27
    