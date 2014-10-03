#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Core
from core.roxxoreditorwidget import *

def registerModule(modulesDict):
    modulesDict['.xml'] = RoxxorEditorXML

class RoxxorEditorXML(RoxxorEditorWidget):

    def __init__(self):
        RoxxorEditorWidget.__init__(self)
