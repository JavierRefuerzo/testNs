#!/usr/bin/env python3
"""
Polyglot v3 node server OpenSprinkler
Copyright (C) 2021 Javier Refuerzo

"""


from curses import nl
import os

from constants.defaultNLS import DefaultNls


class DirModifier :
    

    def __init__(self):

        # There is only one nls, so read the nls template and write the new one
        en_us_txt = "profile/nls/en_us_test.txt"
        self.make_file_dir(en_us_txt)
        nls = open(en_us_txt,  "w")
        test = 0
        while test < 10:
            nls.write("This is a test\n")
            test = test + 1

        nls.write(DefaultNls.nls)
        nls.close()




    def make_file_dir(self, file_path):
        directory = os.path.dirname(file_path)
        if not os.path.exists(directory):
            os.makedirs(directory)
        return True