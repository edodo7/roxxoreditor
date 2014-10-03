#!/usr/bin/python3
# -*- coding: utf-8 -*-

# System
import imp
import sys
import os.path

from PyQt4 import QtCore
from PyQt4 import QtGui

# Core
from core.editor import RoxxorEditorWindow

# Dynamic import of modules
def dynImport():
    modulesDict = {}
    modulesPath = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                               'modules')

    moduleDirs = os.listdir(modulesPath)
    if '__pycache__' in moduleDirs:
        moduleDirs.remove('__pycache__')
    if '.gitignore' in moduleDirs:
        moduleDirs.remove('.gitignore')

    for moduleDir in moduleDirs:
        moduleName = moduleDir + "editorwidget"
        editorFile = moduleName + ".py"
        modulePath = os.path.join(modulesPath, moduleDir, editorFile)

        module = imp.load_source(moduleName, modulePath)
        module.registerModule(modulesDict)

    return modulesDict


def main(modulesDict):
    app = QtGui.QApplication(sys.argv)
    roxxor = RoxxorEditorWindow(modulesDict)
    roxxor.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    modulesDict = dynImport()
    main(modulesDict)
