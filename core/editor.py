#!/bin/python3
# -*- coding: utf-8 -*-

import sys
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
        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.treeWidget)
        self.setLayout(layout)

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    roxxor = RoxxorEditor()
    roxxor.show()
    sys.exit(app.exec_())