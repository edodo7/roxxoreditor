#!/usr/bin/python3
# -*- coding: utf-8 -*-

import json
import os.path

HOME_PATH = os.path.expanduser("~")
ROXXORRC_PATH = os.path.join(HOME_PATH, '.roxxorrc')

def loadRoxxorRc():
    """ Load the configuration located in ~/.roxxorrc. If the file does not
        exists, it is created with engish as default language.
    """
    if os.path.isfile(ROXXORRC_PATH):
        with open(ROXXORRC_PATH, 'r') as rcFile:
            return json.loads(rcFile.read())
    else:
        with open(ROXXORRC_PATH, 'w') as rcFile:
            rcFile.write(json.dumps('{language: "english"}',
                        indent=4, separators=(',', ': ')))
        return {"language": "english"}

def writeRoxxorRc(configuration: dict):
    """ Write the configuration into the ~/.roxxorc file.
    """
    with open(ROXXORRC_PATH, 'w') as rcFile:
        rcFile.write(json.dumps(configuration,
                        indent=4, separators=(',', ': ')))
