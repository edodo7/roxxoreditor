#!/bin/python3
# -*- coding: utf-8 -*-
"""
"""

import sys
from signal import *
from PyQt4 import QtCore
from PyQt4 import QtGui

KEY_LABEL_DEFAULT = "Key: "

class RoxxorEditor(QtGui.QWidget):
    """ The GUI of the editor.
    """
    def __init__(self):
        """
        """
        # TODO wchange when the module is ready
        self.data = {"roxxor": "great",
                     "tamaman": "good",
                     "list": [1,2,3],
                     "dic": {"mydic": "good",
                             "another": {"dico": [True, False, True]}
                            }
                    }
        
        self.key = None
        self.path = []

        QtGui.QWidget.__init__(self)
        self.treeWidget = QtGui.QTreeWidget()
        self.treeWidget.setHeaderHidden(True)
        self.rootItem = QtGui.QTreeWidgetItem()
        self.rootItem.setData(0, 0, "root")
        self.treeWidget.insertTopLevelItem(0, self.rootItem)
        self.connect(self.treeWidget,
                     QtCore.SIGNAL("itemClicked(QTreeWidgetItem*, int)"),
                     self.onClickItem)

        self.loadDataIntoTreeWidget(self.data, self.rootItem)

        # Labels
        self.pathLabel = QtGui.QLabel("/")
        self.keyLabel = QtGui.QLabel(KEY_LABEL_DEFAULT)
        valueLabel = QtGui.QLabel("Value:")

        # Text fields
        self.textField = QtGui.QTextEdit()

        # Buttons
        self.saveModificationsButton = QtGui.QPushButton("Save")
        self.connect(self.saveModificationsButton,
                     QtCore.SIGNAL("clicked()"),
                     self.saveButtonClicked)

        self.leftSubSubLayout = QtGui.QHBoxLayout()
        self.leftSubSubLayout.addWidget(self.treeWidget)
        self.rightSubSubLayout = QtGui.QVBoxLayout()
        self.rightSubSubLayout.addWidget(self.keyLabel)
        self.rightSubSubLayout.addWidget(valueLabel)
        self.rightSubSubLayout.addWidget(self.textField)
        self.rightSubSubLayout.addWidget(self.saveModificationsButton)

        self.subLayout = QtGui.QHBoxLayout()
        self.subLayout.addLayout(self.leftSubSubLayout)
        self.subLayout.addLayout(self.rightSubSubLayout)

        self.layout = QtGui.QVBoxLayout()
        self.layout.addWidget(self.pathLabel)
        self.layout.addLayout(self.subLayout)

        self.setLayout(self.layout)
        self.resize(600, 400)

    def loadDataIntoTreeWidget(self, data, parent):
        """ Load data from a list or a dictionary into the TreeWidget.
        """
        if type(data) == str or type(data) == int or type(data) == bool or type(data) == None:
            item = QtGui.QTreeWidgetItem()
            item.setText(0, str(data))
            parent.addChild(item)
        elif type(data) == list:
            for i in range(len(data)):
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
        if self.isLeaf(item):
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

    def saveButtonClicked(self):
        """ Action performed when the save button is clicked.
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

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    roxxor = RoxxorEditor()
    roxxor.show()
    sys.exit(app.exec_())