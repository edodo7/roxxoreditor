#!/bin/python3
# -*- coding: utf-8 -*-
"""
"""

import sys
from signal import *
from PyQt4 import QtCore
from PyQt4 import QtGui

class RoxxorEditor(QtGui.QWidget):
    """ The GUI of the editor.
    """
    def __init__(self):
        """
        """
        QtGui.QWidget.__init__(self)
        self.treeWidget = QtGui.QTreeWidget()
        self.treeWidget.setHeaderHidden(True)
        self.rootItem = QtGui.QTreeWidgetItem()
        self.rootItem.setData(0, 0, "root")
        self.treeWidget.insertTopLevelItem(0, self.rootItem)
        self.connect(self.treeWidget,
                     QtCore.SIGNAL("itemClicked(QTreeWidgetItem*, int)"),
                     self.onClickItem)
        layout = QtGui.QHBoxLayout()
        layout.addWidget(self.treeWidget)
        layout.addWidget(QtGui.QTextEdit())
        self.setLayout(layout)
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
                    newParent.setText(0, str(key))
                    parent.addChild(newParent)
                    self.loadDataIntoTreeWidget(data[key], newParent)
                elif type(data[key]) == list:
                    newParent = QtGui.QTreeWidgetItem()
                    newParent.setText(0, str(key))
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
            path.insert(0, parent.text(0))
        while parent != None:
            parent = parent.parent()
            if parent != None:
                path.insert(0, parent.text(0))
        return path

    def onClickItem(self, item: QtGui.QTreeWidgetItem, i):
        """
        """
        print(self.getTreePath(item))

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    roxxor = RoxxorEditor()
    # roxxor.loadDataIntoTreeWidget([[1,1,1],[2],3,4,5], roxxor.rootItem)
    roxxor.loadDataIntoTreeWidget({"roxxor": "great",
                                   "tamaman": "good",
                                   "list": [1,2,3],
                                   "dic": {"mydic": "good",
                                           "another": {"dico": [True, False, True]}
                                          }
                                   }, roxxor.rootItem)
    roxxor.show()
    sys.exit(app.exec_())