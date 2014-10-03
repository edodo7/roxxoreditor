#!/usr/bin/python3
# -*- coding: utf-8 -*-

from PyQt4 import QtCore
from PyQt4 import QtGui

from core.dialog import errorDialog

class RoxxorEditorWidget(QtGui.QWidget):

    def __init__(self):
        QtGui.QWidget.__init__(self)

    def setData(self, filename):
        errorDialog('Function not implemented yet!')

    def read(self, filename):
        errorDialog('Function not implemented yet!')

    def write(self, filename, content):
        errorDialog('Function not implemented yet!')
