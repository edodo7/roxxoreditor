#!/usr/bin/python3
# -*- coding: utf-8 -*-

# System
import json
import copy
from PyQt4 import QtCore
from PyQt4 import QtGui

# Core
from core.dialog import *
from core.roxxoreditorwidget import *
# Modules JSON
from modules.json.displayerwidget import TreeWidgetJSON
from modules.json.displayerwidget import TreeWidgetItemJSON
from modules.json.tools import extractDataStructure

# CONSTANTS
KEY_LABEL_DEFAULT = "Key: "
RESTORE_BUTTON_DEFAULT = "Restore original value"

def registerModule(modulesDict):
    modulesDict['.json'] = RoxxorEditorJSON

class RoxxorEditorJSON(RoxxorEditorWidget):
    """ The GUI of the editor for JSON.
    """
    def __init__(self):
        """ Initialization of the object.
        """
        # This variable is the backup of the data
        self.originalData = {}
        # This variable is the data user work with
        self.data = {}

        self.key = None
        self.path = []

        QtGui.QWidget.__init__(self)

        # Tree widget
        self.treeWidget = TreeWidgetJSON(self)
        self.connect(self.treeWidget,
                     QtCore.SIGNAL("itemClicked(QTreeWidgetItem*, int)"),
                     self.onClickItem)

        # Labels
        self.pathLabel = QtGui.QLabel("/")
        self.pathLabel.setSizePolicy(QtGui.QSizePolicy.Minimum,
                                     QtGui.QSizePolicy.Maximum)
        self.keyLabel = QtGui.QLabel(KEY_LABEL_DEFAULT)
        self.keyLabel.hide()
        self.valueLabel = QtGui.QLabel("Value:")
        self.valueLabel.hide()

        # Input widget
        self.stringWidget = QtGui.QTextEdit()
        self.booleanWidget = QtGui.QComboBox(self)
        self.booleanWidget.setMaximumSize(QtCore.QSize(150,40))
        self.booleanWidget.addItem("True")
        self.booleanWidget.addItem("False")
        self.noneWidget = QtGui.QLabel("None")
        self.noneWidget.setMaximumSize(QtCore.QSize(150,40))
        self.integerWidget = QtGui.QLineEdit()
        self.integerWidget.setMaximumSize(QtCore.QSize(150,40))
        self.integerWidget.setValidator(QtGui.QIntValidator(self))
        self.floatWidget = QtGui.QLineEdit()
        self.floatWidget.setMaximumSize(QtCore.QSize(150,40))
        self.floatWidget.setValidator(QtGui.QDoubleValidator(self))
        # Input widget layout
        self.inputWidgetLayout = QtGui.QStackedLayout()
        self.inputWidgetLayout.addWidget(self.stringWidget)
        self.inputWidgetLayout.addWidget(self.booleanWidget)
        self.inputWidgetLayout.addWidget(self.noneWidget)
        self.inputWidgetLayout.addWidget(self.integerWidget)
        self.inputWidgetLayout.addWidget(self.floatWidget)
        self.inputWidgetLayout.currentWidget().hide()

        # Buttons
        self.modificationsButton = QtGui.QPushButton(RESTORE_BUTTON_DEFAULT)
        self.connect(self.modificationsButton,
                     QtCore.SIGNAL("clicked()"),
                     self.restoreButtonClicked)
        self.modificationsButton.hide()

        # Layouts
        topRightSubSubSubLayout = QtGui.QHBoxLayout()
        topRightSubSubSubLayout.addWidget(self.keyLabel)

        leftSubSubLayout = QtGui.QHBoxLayout()
        leftSubSubLayout.addWidget(self.treeWidget)

        rightSubSubLayout = QtGui.QVBoxLayout()
        rightSubSubLayout.addLayout(topRightSubSubSubLayout)
        rightSubSubLayout.addWidget(self.valueLabel)
        rightSubSubLayout.addLayout(self.inputWidgetLayout)
        rightSubSubLayout.addWidget(self.modificationsButton)

        leftFrame = QtGui.QFrame()
        leftFrame.setLayout(leftSubSubLayout)
        rightFrame = QtGui.QFrame()
        rightFrame.setLayout(rightSubSubLayout)

        splitter = QtGui.QSplitter(QtCore.Qt.Horizontal)
        splitter.addWidget(leftFrame)
        splitter.addWidget(rightFrame)

        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.pathLabel)
        layout.addWidget(splitter)

        self.setLayout(layout)

    def currentInputWidget(self):
        """ Return the input widget currently shown to the user.
        """
        return self.inputWidgetLayout.currentWidget()

    def onClickItem(self, item: QtGui.QTreeWidgetItem, column: int):
        """ Action performed when an item in the QTreeWidget is clicked.

        Keyword arguments:
            item   -- The item user clicked on.
            column -- The column number clicked (not used here).
        """
        if self.path and self.key != None:
            self.saveValue()
        if self.data and self.treeWidget.isLeaf(item) and len(item.text(0).split()) == 1:
            dataSought = self.data
            self.path = self.treeWidget.getTreePath(item)
            for element in self.path:
                try:
                    i = int(element)
                    dataSought = dataSought[i]
                except ValueError:
                    dataSought = dataSought[element]
            self.key = self.path[len(self.path)-1]
            self.keyLabel.setText(KEY_LABEL_DEFAULT+str(self.key))
            self.pathLabel.setText("/"+'>'.join([ str(p) for p in self.path]))
            if dataSought == None:
                self.inputWidgetLayout.setCurrentWidget(self.noneWidget)
            elif type(dataSought) == int:
                self.integerWidget.setText(str(dataSought))
                self.inputWidgetLayout.setCurrentWidget(self.integerWidget)
            elif type(dataSought) == float:
                self.floatWidget.setText(str(dataSought))
                self.inputWidgetLayout.setCurrentWidget(self.floatWidget)
            elif type(dataSought) == str:
                self.stringWidget.setText(dataSought)
                self.inputWidgetLayout.setCurrentWidget(self.stringWidget)
            elif type(dataSought) == bool:
                self.booleanWidget.setEditText(str(dataSought))
                self.inputWidgetLayout.setCurrentWidget(self.booleanWidget)
            self.keyLabel.show()
            self.valueLabel.show()
            self.inputWidgetLayout.currentWidget().show()
            self.modificationsButton.show()
        else:
            # Key Label
            self.keyLabel.setText(KEY_LABEL_DEFAULT)

            # Update path
            self.path = self.treeWidget.getTreePath(item)
            self.pathLabel.setText("/"+'>'.join([ str(p) for p in self.path ]))

            self.keyLabel.hide()
            self.valueLabel.hide()
            self.currentInputWidget().hide()
            self.modificationsButton.hide()

            self.key = None

    def restoreButtonClicked(self):
        """ Action performed when the restore button is clicked.
        """
        subPath = self.path[0:len(self.path)-1]
        dataStruct = extractDataStructure(self.originalData, subPath)
        if dataStruct[self.key] == None:
            self.inputWidgetLayout.setCurrentWidget(self.noneWidget)
        elif type(dataStruct[self.key]) == int:
            self.integerWidget.setText(str(dataStruct[self.key]))
            self.inputWidgetLayout.setCurrentWidget(self.integerWidget)
        elif type(dataStruct[self.key]) == float:
            self.floatWidget.setText(str(dataStruct[self.key]))
            self.inputWidgetLayout.setCurrentWidget(self.floatWidget)
        elif type(dataStruct[self.key]) == str:
            self.stringWidget.setText(dataStruct[self.key])
            self.inputWidgetLayout.setCurrentWidget(self.stringWidget)
        elif type(dataStruct[self.key]) == bool:
            self.booleanWidget.setEditText(str(dataStruct[self.key]))
            self.inputWidgetLayout.setCurrentWidget(self.booleanWidget)

    def saveValue(self):
        """ Save the value that has been modified precedently in the memory.
        """
        subPath = self.path[0:len(self.path)-1]
        dataStruct = dataStruct = extractDataStructure(self.data, subPath)
        originalDataStruct = extractDataStructure(self.originalData, subPath)
        try:
            if originalDataStruct[self.key] != None: # From now you can not edit the type.
                oldType = type(originalDataStruct[self.key])
                if oldType == int:
                    dataStruct[self.key] = int(self.integerWidget.text())
                elif oldType == float:
                    dataStruct[self.key] = float(self.floatWidget.text())
                elif oldType == str:
                    dataStruct[self.key] = self.stringWidget.toPlainText()
                elif oldType == bool:
                    if self.booleanWidget.currentText() == "True":
                        dataStruct[self.key] = True
                    else:
                        dataStruct[self.key] = False

        except ValueError:
            errorDialog("Wrong entry!")

    def resetData(self):
        """ Reset the data to create a new empty file.
        """
        self.originalData = {}
        self.data = {}
        self.key = None
        self.path = []
        self.pathLabel.setText("/")
        self.treeWidget.recreateEmptyTreeView()

    def setData(self, filename):
        """ Set the instance variable self.data and refresh the tree view.

        Keyword arguments:
            filename -- The name of the file with the contents to process.
        """
        self.originalData = self.read(filename)
        self.data = copy.deepcopy(self.originalData)
        self.key = None
        self.path = []
        self.pathLabel.setText("/")
        self.treeWidget.recreateTreeView(self.data)

    def read(self, filename):
        """ Reads the file specified by the filename and returns the content
            as a python dict.

        Keyword arguments:
            filename -- The name of the file with the contents to process.
        """
        with open(filename, 'r') as finput:
            content = json.loads(finput.read())
        return content


    def write(self, filename, content):
        """ Writes the given content into the specified filename.

        Keyword arguments:
            filename -- The name of the file in which the contents will be write.
            content  -- The content to write into the file.
        """
        str_dump = json.dumps(content, indent=4, separators=(',', ': '))

        with open(filename, 'w') as foutput:
            foutput.writelines(str_dump)

        self.originalData = copy.deepcopy(self.data)
