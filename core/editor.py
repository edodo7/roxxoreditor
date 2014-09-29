#!/bin/python3
# -*- coding: utf-8 -*-
""" This script contains the core of the Roxxor Editor.
"""

import imp
import sys
import os.path
from PyQt4 import QtCore
from PyQt4 import QtGui

from dialog import aboutDialog, modulesDialog

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

        self.fileName = ""

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

        self.displayStatus('Roxxor Editor ready!', 3)


    def displayStatus(self, status, delay=5):
        """ Display the specified message status in the status bar
            for 'delay' seconds.

        Keyword arguments:
            status -- The message to display in the status bar.
            delay  -- The number of seconds the message must be displayed.
        """
        self.statusBar().showMessage(status, delay * 1000)


    def openFile(self):
        """ The action performed when the button "Open" in the tool bar
            is clicked.
        """
        self.fileName = QtGui.QFileDialog.getOpenFileName(self, 'Open a file',
                        str(os.path.expanduser("~")))

        base, ext = os.path.splitext(self.fileName)

        if base != "":
            ext = self.updateModule(ext)

        if ext != None and self.fileName != "":
            # Read and Set datas
            self.roxxorWidget.setData(self.fileName)
            self.displayStatus('File \'' + os.path.split(self.fileName)[1] +
                               '\' loaded with the module \'' +
                               self.activeWidget[1:].upper() + '\'.')
        else:
            self.displayStatus('Open file cancelled.')


    def updateModule(self, ext):
        """ Update the module to use, may ask the user the module to use.

        Keyword arguments:
            ext -- The extension of the selected file.
        """
        # Extension not known by Roxxor; ask the user which module to use
        if ext not in modulesDict.keys():
            ext = modulesDialog(modulesDict.keys())

        # Module has changed; load the new one
        if ext != None and ext != self.activeWidget:
            self.activeWidget = ext.lower()
            self.roxxorWidget = modulesDict[self.activeWidget]()
            self.setCentralWidget(self.roxxorWidget)

        return ext


    def saveFile(self):
        """ The action performed when the button "Save" in the menubar
            is clicked.
        """
        if self.fileName == "":
            self.fileName = QtGui.QFileDialog.getSaveFileName(self, "Save file")

        if self.fileName != "":
            self.roxxorWidget.write(self.fileName, self.roxxorWidget.data)
            self.displayStatus('File \'' + os.path.split(self.fileName)[1] +
                               '\' saved.')


    def saveAsFile(self):
        """ The action performed when the button "Save as..." in the menubar
            is clicked.
        """
        self.fileName = QtGui.QFileDialog.getSaveFileName(self, "Save file as...")

        if self.fileName != "":
            self.roxxorWidget.write(self.fileName, self.roxxorWidget.data)
            self.displayStatus('File \'' + os.path.split(self.fileName)[1] +
                               '\' saved.')


def main():
    app = QtGui.QApplication(sys.argv)
    roxxor = RoxxorEditorWindow()
    roxxor.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
