#!/bin/python3
# -*- coding: utf-8 -*-
""" This script contains the core of the Roxxor Editor.
"""

import sys
import os.path
import imp
from signal import *
from PyQt4 import QtCore
from PyQt4 import QtGui

KEY_LABEL_DEFAULT = "Key: "
RESTORE_BUTTON_DEFAULT = "Restore old value"
ADD_BUTTON_DEFAULT = "Add a key"

class RoxxorEditorWidget(QtGui.QWidget):
    """ The GUI of the editor.
    """
    def __init__(self):
        """ Initialization of the object.
        """
        self.data = {}

        self.key = None
        self.path = []

        QtGui.QWidget.__init__(self)
        self.treeWidget = QtGui.QTreeWidget()
        self.treeWidget.setHeaderHidden(True)
        self.treeWidget.setAlternatingRowColors(True)
        self.rootItem = QtGui.QTreeWidgetItem()
        self.rootItem.setData(0, 0, "root")
        self.treeWidget.insertTopLevelItem(0, self.rootItem)
        self.connect(self.treeWidget,
                     QtCore.SIGNAL("itemClicked(QTreeWidgetItem*, int)"),
                     self.onClickItem)

        # Labels
        self.pathLabel = QtGui.QLabel("/")
        self.keyLabel = QtGui.QLabel(KEY_LABEL_DEFAULT)
        valueLabel = QtGui.QLabel("Value:")

        # Text fields
        self.textField = QtGui.QTextEdit()
        self.keyTextField = QtGui.QLineEdit()

        # Buttons
        self.modificationsButton = QtGui.QPushButton(ADD_BUTTON_DEFAULT)
        self.connect(self.modificationsButton,
                     QtCore.SIGNAL("clicked()"),
                     self.addButtonClicked)

        # Layouts
        self.topRightSubSubSubLayout = QtGui.QHBoxLayout()
        self.topRightSubSubSubLayout.addWidget(self.keyLabel)
        self.topRightSubSubSubLayout.addWidget(self.keyTextField)

        self.leftSubSubLayout = QtGui.QHBoxLayout()
        self.leftSubSubLayout.addWidget(self.treeWidget)

        self.rightSubSubLayout = QtGui.QVBoxLayout()
        self.rightSubSubLayout.addLayout(self.topRightSubSubSubLayout)
        self.rightSubSubLayout.addWidget(valueLabel)
        self.rightSubSubLayout.addWidget(self.textField)
        self.rightSubSubLayout.addWidget(self.modificationsButton)

        self.subLayout = QtGui.QHBoxLayout()
        self.subLayout.addLayout(self.leftSubSubLayout)
        self.subLayout.addLayout(self.rightSubSubLayout)

        self.layout = QtGui.QVBoxLayout()
        self.layout.addWidget(self.pathLabel)
        self.layout.addLayout(self.subLayout)

        self.setLayout(self.layout)

    def loadDataIntoTreeWidget(self, data, parent, force_explore=None):
        """ Load data from a list or a dictionary into the TreeWidget.
        """
        if type(data) == str or type(data) == int or type(data) == bool or data == None:
            item = QtGui.QTreeWidgetItem()
            item.setText(0, str(data))
            parent.addChild(item)
            if force_explore:
                self.loadDataIntoTreeWidget(force_explore[data], item)
        elif type(data) == list:
            for i in range(len(data)):
                if type(data[i]) == dict or type(data[i]) == list:
                    self.loadDataIntoTreeWidget(i, parent, data)
                else:
                    self.loadDataIntoTreeWidget(i, parent)
        elif type(data) == dict:
            for key in data.keys():
                if type(data[key]) == dict:
                    newParent = QtGui.QTreeWidgetItem()
                    newParent.setText(0, str(key)+" {}")
                    parent.addChild(newParent)
                    self.loadDataIntoTreeWidget(data[key], newParent)
                elif type(data[key]) == list:
                    newParent = QtGui.QTreeWidgetItem()
                    newParent.setText(0, str(key)+" []")
                    parent.addChild(newParent)
                    self.loadDataIntoTreeWidget(data[key], newParent)
                else:
                    self.loadDataIntoTreeWidget(key, parent)
        else:
            raise TypeError

    def getTreePath(self, item: QtGui.QTreeWidgetItem):
        """ Return the list of ancestors of the item passed in parameters
            (itself included) sorted in ascending order.
        """
        path = [item.text(0)]
        parent = item.parent()
        if parent != None:
            path.insert(0, parent.text(0).split()[0])
        while parent != None:
            parent = parent.parent()
            if parent != None:
                path.insert(0, parent.text(0).split()[0])
        path.pop(0)
        return path

    def onClickItem(self, item: QtGui.QTreeWidgetItem, i):
        """ Action performed when an item in the QTreeWidget is clicked.
        """
        if self.path:
            self.saveValue()
        if self.data and self.isLeaf(item):
            self.modificationsButton.clicked.disconnect()
            self.modificationsButton.setText(RESTORE_BUTTON_DEFAULT)
            self.connect(self.modificationsButton,
                         QtCore.SIGNAL("clicked()"),
                         self.restoreButtonClicked)
            self.keyTextField.setText("")
            self.keyTextField.hide()

            dataSought = self.data
            self.path = self.getTreePath(item)
            for element in self.path:
                try:
                    i = int(element)
                    dataSought = dataSought[i]
                except ValueError:
                    dataSought = dataSought[element]
            self.key = self.path[len(self.path)-1]
            self.keyLabel.setText(KEY_LABEL_DEFAULT+str(self.key))
            self.pathLabel.setText("/"+'>'.join(self.path))
            self.textField.setText(str(dataSought))
        else:
            # Key Label
            self.keyLabel.setText(KEY_LABEL_DEFAULT)
            self.keyTextField.show()

            # Button
            self.modificationsButton.clicked.disconnect()
            self.modificationsButton.setText(ADD_BUTTON_DEFAULT)
            self.connect(self.modificationsButton,
                         QtCore.SIGNAL("clicked()"),
                         self.addButtonClicked)
            self.modificationsButton.setText(ADD_BUTTON_DEFAULT)

    def restoreButtonClicked(self):
        """ Action performed when the restore button is clicked.
        """
        dataStruct = self.data
        for i in range(len(self.path)-1):
            try:
                j = int(self.path[i])
                dataStruct = dataStruct[j]
            except ValueError:
                dataStruct = dataStruct[self.path[i]]
        try:
            self.textField.setText(str(dataStruct[int(self.key)]))
        except ValueError:
            self.textField.setText(str(dataStruct[self.key]))

    def addButtonClicked(self):
        """ Action performed when the add button is clicked
        """
        dataStruct = self.data
        for i in range(len(self.path)-1):
            try:
                j = int(self.path[i])
                dataStruct = dataStruct[j]
            except ValueError:
                dataStruct = dataStruct[self.path[i]]
        self.key = self.keyTextField.text()
        data = self.textField.toPlainText()
        if self.key != "":
            if type(dataStruct) == list:
                try:
                    i = int(self.key)
                    dataStruct[i] = data
                except ValueError:
                    print("The index must be an integer!") # TODO popup
            elif type(dataStruct) == dict:
                dataStruct[self.key] = data

            for i in range(self.rootItem.childCount()):
                self.rootItem.removeChild(self.rootItem.child(i))

            self.setData(self.data)
        else:
            print("A key can't be empty!") # TODO popup

    def saveValue(self):
        """ Save the value that has been modified precedently in the memory.
        """
        dataStruct = self.data
        for i in range(len(self.path)-1):
            try:
                j = int(self.path[i])
                dataStruct = dataStruct[j]
            except ValueError:
                dataStruct = dataStruct[self.path[i]]
        try:
            try:
                oldType = type(dataStruct[int(self.key)])
                dataStruct[int(self.key)] = oldType(self.textField.toPlainText())
            except ValueError:
                oldType = type(dataStruct[self.key])
                dataStruct[self.key] = oldType(self.textField.toPlainText())
        except TypeError:
            try:
                self.textField.setText(str(dataStruct[int(self.key)]))
            except ValueError:
                self.textField.setText(str(dataStruct[self.key]))
            print("Wrong entry") # TODO popup

    def isLeaf(self, item: QtGui.QTreeWidgetItem):
        """ Return True if the item is a leaf of the QTreeWidget else
            return False.
        """
        return item.childCount() == 0

    def setData(self, data):
        """ Set the instance variable self.data and refresh the tree view.
        """
        self.data = data
        self.key = None
        self.path = []
        self.pathLabel.setText("/")
        # "Destroy" old root and create a new one
        self.treeWidget.takeTopLevelItem(0)
        self.rootItem = QtGui.QTreeWidgetItem()
        self.rootItem.setData(0, 0, "root")
        self.treeWidget.insertTopLevelItem(0, self.rootItem)
        # Load data into the tree and sort it
        self.loadDataIntoTreeWidget(self.data, self.rootItem)
        self.treeWidget.sortItems(0,0)
        self.rootItem.setExpanded(True)

class RoxxorEditorWindow(QtGui.QMainWindow):
    """ The main window of the editor.
    """
    def __init__(self):
        """ Initialization of the object.
        """
        QtGui.QMainWindow.__init__(self)
        self.setWindowTitle("Roxxor Editor")
        self.roxxorWidget = RoxxorEditorWidget()
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
        saveAction.triggered.connect(self.saveModifications)

        exitAction = QtGui.QAction('Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(self.close)

        # Tool bar
        toolBar = self.addToolBar('Open')
        toolBar.setMovable(False)

        toolBar.addAction(openAction)
        toolBar.addAction(saveAction)
        toolBar.addAction(exitAction)

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
            # TODO
            modulePath = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                                      '..',
                                                      'modules',
                                                      'jsontools.py')
            jsontools = imp.load_source('jsontools', modulePath)

            self.roxxorWidget.setData(jsontools.read(self.fileName))
        else:
            self.fileName = None

    def saveModifications(self):
        """ The action performed when the button "Save" un the tool bar
            is clicked.
        """
        # TODO
        modulePath = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                                  '..',
                                                  'modules',
                                                  'jsontools.py')
        jsontools = imp.load_source('jsontools', modulePath)

        jsontools.write(self.fileName, self.roxxorWidget.data)

def main():
    app = QtGui.QApplication(sys.argv)
    roxxor = RoxxorEditorWindow()
    roxxor.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
