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
    none = 0
    password = 1
    ipAddress = 2
    connection = 3
    checkLogs = 4
    invalidUrl = 5
    firmware = 6