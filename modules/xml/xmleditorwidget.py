#!/bin/python3
# -*- coding: utf-8 -*-

from roxxoreditorwidget import *

def registerModule(modulesDict):
    modulesDict['.xml'] = RoxxorEditorXML

class RoxxorEditorXML(RoxxorEditorWidget):

    def __init__(self):
        RoxxorEditorWidget.__init__(self)
