#!/bin/python3
# -*- coding: utf-8 -*-

import sys
from signal import *
from PyQt4 import QtCore
from PyQt4 import QtGui

"""
"""
class RoxxorEditor(QtGui.QWidget):
    """
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
        self.connect (self.treeWidget, QtCore.SIGNAL ("itemClicked(QTreeWidgetItem*, int)"), self.onClickItem)
        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.treeWidget)
        self.setLayout(layout)
        self.resize(600, 400)

    def loadData(self, data, parent):
        """
        """
        if type(data) == str or type(data) == int or type(data) == bool or type(data) == None:
            item = QtGui.QTreeWidgetItem()
            item.setText(0, str(data))
            parent.addChild(item)
        elif type(data) == list:
            for i in range(len(data)):
                self.loadData(i, parent)
        elif type(data) == dict:
            for key in data.keys():
                if type(data[key]) == dict:
                    newParent = QtGui.QTreeWidgetItem()
                    newParent.setText(0, str(key))
                    parent.addChild(newParent)
                    self.loadData(data[key], newParent)
                elif type(data[key]) == list:
                    newParent = QtGui.QTreeWidgetItem()
                    newParent.setText(0, str(key))
                    parent.addChild(newParent)
                    self.loadData(data[key], newParent)
                else:
                    self.loadData(key, parent)
        else:
            raise TypeError

    def onClickItem(self, item, i):
        """
        """
        print(str(item.text(0)))
        print(str(item.parent().text(0)))

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    roxxor = RoxxorEditor()
    roxxor.show()
    sys.exit(app.exec_())