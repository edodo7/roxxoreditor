#!/usr/bin/python3
# -*- coding: utf-8 -*-
""" This script contains the core of the Roxxor Editor.
"""

# System
import os.path

from PyQt4 import QtCore
from PyQt4 import QtGui

# Core
from core.dialog import aboutDialog
from core.dialog import modulesDialog


class RoxxorEditorWindow(QtGui.QMainWindow):
    """ The main window of the editor.
    """
    def __init__(self, modulesDict):
        """ Initialization of the object.
        """
        QtGui.QMainWindow.__init__(self)
        self.setWindowTitle("Roxxor Editor")

        self.fileName = ""
        self.modulesDict = modulesDict

        self.activeWidget = '.json'
        self.roxxorWidget = self.modulesDict[self.activeWidget]()
        self.setCentralWidget(self.roxxorWidget)

        # Actions
        newAction = QtGui.QAction('New File', self)
        newAction.setShortcut('Ctrl+N')
        newAction.setStatusTip('Create a new file')
        newAction.triggered.connect(self.newFile)

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

        # findAction = QtGui.QAction('Find...', self)
        # findAction.setShortcut('Ctrl+F')
        # findAction.setStatusTip('Search key/value')
        # findAction.triggered.connect(self.findKeyValue)

        aboutAction = QtGui.QAction('About', self)
        aboutAction.setShortcut('F1')
        aboutAction.setStatusTip('Application informations')
        aboutAction.triggered.connect(aboutDialog)

        # Menu Bar
        menubar = self.menuBar()

        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(newAction)
        fileMenu.addAction(openAction)
        fileMenu.addAction(saveAction)
        fileMenu.addAction(saveAsAction)
        fileMenu.addSeparator()
        fileMenu.addAction(exitAction)

        # fileMenu = menubar.addMenu('Fi&nd')
        # fileMenu.addAction(findAction)

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


    def newFile(self):
        """ The action performed when the button "New File" in the tool bar
            is clicked.
        """
        ext = self.updateModule()

        if ext != None:
            # Reset Data
            self.roxxorWidget.resetData()
            self.displayStatus('New file opened.')
        else:
            self.displayStatus('New file cancelled.')


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


    def updateModule(self, ext=""):
        """ Update the module to use, may ask the user the module to use.

        Keyword arguments:
            ext -- The extension of the selected file.
        """
        # Extension not known by Roxxor; ask the user which module to use
        if ext not in self.modulesDict.keys():
            ext = modulesDialog(self.modulesDict.keys())

        # Module has changed; load the new one
        if ext != None and ext != self.activeWidget:
            self.activeWidget = ext.lower()
            self.roxxorWidget = self.modulesDict[self.activeWidget]()
            self.setCentralWidget(self.roxxorWidget)

        return ext


    def saveFile(self):
        """ The action performed when the button "Save" in the menubar
            is clicked.
        """
        if self.fileName == "":
            self.fileName = QtGui.QFileDialog.getSaveFileName(self, "Save file")

        if self.fileName != "":
            # Save the value that is being edited
            self.roxxorWidget.saveValue()
            # Write in the file
            self.roxxorWidget.write(self.fileName, self.roxxorWidget.data)
            self.displayStatus('File \'' + os.path.split(self.fileName)[1] +
                               '\' saved.')


    def saveAsFile(self):
        """ The action performed when the button "Save as..." in the menubar
            is clicked.
        """
        self.fileName = QtGui.QFileDialog.getSaveFileName(self, "Save file as...")

        if self.fileName != "":
            # Save the value that is being edited
            self.roxxorWidget.saveValue()
            # Write in the file
            self.roxxorWidget.write(self.fileName, self.roxxorWidget.data)
            self.displayStatus('File \'' + os.path.split(self.fileName)[1] +
                               '\' saved.')
