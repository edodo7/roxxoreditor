#!/bin/python3
# -*- coding: utf-8 -*-
""" This script contains the core of the Roxxor Editor.
"""

import sys
import os.path
import imp
from PyQt4 import QtCore
from PyQt4 import QtGui

from dialog import aboutDialog

# Dynamic import of modules
modulesDict = {}
modulesPath = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                          '..',
                                          'modules')
moduleFiles = os.listdir(modulesPath)

for moduleFile in moduleFiles:
    if moduleFile.endswith('tools.py'):
        moduleName = moduleFile[:-3]
        modulePath = os.path.join(modulesPath, moduleFile)

        module = imp.load_source(moduleName, modulePath)
        module.registerModule(modulesDict)


class RoxxorEditorWindow(QtGui.QMainWindow):
    """ The main window of the editor.
    """
    def __init__(self):
        """ Initialization of the object.
        """
        QtGui.QMainWindow.__init__(self)
        self.setWindowTitle("Roxxor Editor")
        self.activeWidget = '.json'
        self.roxxorWidget = modulesDict[self.activeWidget]()
        self.setCentralWidget(self.roxxorWidget)

        self.fileName = None

        # Actions
        openAction = QtGui.QAction('Open', self)
        openAction.setShortcut('Ctrl+O')
        openAction.setStatusTip('Open a file')
        openAction.triggered.connect(self.openFile)

        saveAction = QtGui.QAction('Save', self)
        saveAction.setShortcut('Ctrl+S')
        saveAction.setStatusTip('Save the modifications')
        saveAction.triggered.connect(self.saveFile)

        saveAsAction = QtGui.QAction('Save As...', self)
        saveAsAction.setShortcut('Ctrl+Shift+S')
        saveAsAction.setStatusTip('Save the modifications')
        saveAsAction.triggered.connect(self.saveAsFile)

        exitAction = QtGui.QAction('Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(self.close)

        aboutAction = QtGui.QAction('About', self)
        aboutAction.setShortcut('F1')
        aboutAction.setStatusTip('Application informations')
        aboutAction.triggered.connect(aboutDialog)

        # Menu Bar
        menubar = self.menuBar()

        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(openAction)
        fileMenu.addAction(saveAction)
        fileMenu.addAction(saveAsAction)
        fileMenu.addSeparator()
        fileMenu.addAction(exitAction)

        fileMenu = menubar.addMenu('&Help')
        fileMenu.addAction(aboutAction)

        self.resize(800, 400)
        # Put the window on the center of the screen
        self.move(QtGui.QApplication.desktop().screen().rect().center()-
                  self.rect().center())

    def openFile(self):
        """ The action performed when the button "Open" in the tool bar
            is clicked.
        """
        self.fileName = QtGui.QFileDialog.getOpenFileName(self, 'Open a file',
                        str(os.path.expanduser("~")))
        if self.fileName != "":
            # Actualize widget following the extension of the file to use
            ext = os.path.splitext(self.fileName)[1]
            if ext != self.activeWidget:
                self.activeWidget = ext
                self.roxxorWidget = modulesDict[self.activeWidget]()
                self.setCentralWidget(self.roxxorWidget)

            # Read and Set datas
            self.roxxorWidget.setData(self.fileName)
        else:
            self.fileName = None

    def saveFile(self):
        """ The action performed when the button "Save" un the tool bar
            is clicked.
        """
        if self.fileName == None:
            self.fileName = QtGui.QFileDialog.getSaveFileName(self, "Save file")

        if self.fileName != "":
            self.roxxorWidget.write(self.fileName, self.roxxorWidget.data)
        else:
            self.fileName = None

    def saveAsFile(self):
        """ The action performed when the button "Save" un the tool bar
            is clicked.
        """
        self.fileName = QtGui.QFileDialog.getSaveFileName(self, "Save file as...")

        if self.fileName != "":
            self.roxxorWidget.write(self.fileName, self.roxxorWidget.data)
        else:
            self.fileName = None

def main():
    app = QtGui.QApplication(sys.argv)
    roxxor = RoxxorEditorWindow()
    roxxor.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
