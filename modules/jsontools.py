#!/bin/python3
# -*- coding: utf-8 -*-

import json
import copy
from roxxoreditorwidget import *
from dialog import *

from PyQt4 import QtCore
from PyQt4 import QtGui

def registerModule(modulesDict):
    modulesDict['.json'] = RoxxorEditorJSON

def askForKey():
    """ Create and display a dialog that ask to the user the key name.
    """
    key, ok = QtGui.QInputDialog.getText(None, 'Key name', 
            'Enter the key name:')
    return key, ok

def askForData():
    """ Create and display a dialog that ask to the user the data.
    """
    ok, dataType, data = DataDialog().exec_()
    if dataType == None:
        data = None
    else:
        try:
            data = dataType(data)
        except ValueError:
            errorDialog("The data typed does not correspond to the type choosen.")
            ok = False
    return data, ok

def askForIndex(minimum: int, maximum: int):
    """ Create and display a dialog that ask to the user an index.

    Keyword arguments:
        minimum -- Lower boundary of the index choice.
        maximum -- Higher boundary of the index choice.
    """
    index, ok = QtGui.QInputDialog.getInteger(None, 'Index', 
            'Enter the index:', value=maximum, min=minimum, max=maximum)
    return index, ok

def isConfirmed(description: str):
    """ Create and display a dialog that ask to the user if he confirm
        the action described in the string in parameter.

    Keyword arguments:
        description -- The description of what have to be confirmed.
    """
    reply = QtGui.QMessageBox.question(None, 'Confirmation',
                            description,
                            QtGui.QMessageBox.Yes |
                            QtGui.QMessageBox.No, QtGui.QMessageBox.No)
    if reply == QtGui.QMessageBox.Yes:
        return True
    return False

KEY_LABEL_DEFAULT = "Key: "
RESTORE_BUTTON_DEFAULT = "Restore original value"

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

        # Text fields
        self.textField = QtGui.QTextEdit()
        self.textField.hide()

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
        rightSubSubLayout.addWidget(self.textField)
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

    def extractDataStructure(self, dataStruct, path: list):
        """ Extract the sub data structure defined by the path from dataStruct.

        Keyword arguments:
            dataStruct -- The data structure in wich we search for the sub data
                          structure.
            path       -- The path to the sub data structure.
        """
        for i in range(len(path)):
            try:
                j = int(path[i])
                dataStruct = dataStruct[j]
            except ValueError:
                dataStruct = dataStruct[path[i]]
        return dataStruct

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
            self.textField.setText(str(dataSought))
            self.keyLabel.show()
            self.valueLabel.show()
            self.textField.show()
            self.modificationsButton.show()
        else:
            # Key Label
            self.keyLabel.setText(KEY_LABEL_DEFAULT)

            # Update path
            self.path = self.treeWidget.getTreePath(item)
            self.pathLabel.setText("/"+'>'.join([ str(p) for p in self.path ]))

            self.keyLabel.hide()
            self.valueLabel.hide()
            self.textField.hide()
            self.modificationsButton.hide()

            self.key = None

    def restoreButtonClicked(self):
        """ Action performed when the restore button is clicked.
        """
        subPath = self.path[0:len(self.originalData)-1]
        dataStruct = self.extractDataStructure(self.originalData, subPath)
        self.textField.setText(str(dataStruct[self.key]))

    def saveValue(self):
        """ Save the value that has been modified precedently in the memory.
        """
        subPath = self.path[0:len(self.originalData)-1]
        dataStruct = self.extractDataStructure(self.originalData, subPath)
        try:
            oldType = type(dataStruct[self.key])
            dataStruct[self.key] = oldType(self.textField.toPlainText())
        except ValueError:
            self.textField.setText(str(dataStruct[self.key]))
            errorDialog("Wrong entry!")

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

class TreeWidgetItemJSON(QtGui.QTreeWidgetItem):
    """ A tree widget item specialised for displaying JSON data.
    """
    def __init__(self, data, dataType=None):
        """ Initialization of the object.

        Keyword arguments:
            data     -- The data that will contain the tree widget item.
            dataType -- The data's type. If not a list or a dict, leave setted
                        to None.
        """
        QtGui.QTreeWidgetItem.__init__(self)
        self.data = data
        self.dataType = dataType
        self.setText()

    def setText(self):
        """ Overload the original method by creating the string according
            to the dataType. If it is a list add "[]" after the data, if it
            is a dict add "{}" after the data.
        """
        s = str(self.data)
        if self.dataType == list:
            s += " []"
        elif self.dataType == dict:
            s += " {}"
        QtGui.QTreeWidgetItem.setText(self, 0, s)

class TreeWidgetJSON(QtGui.QTreeWidget):
    """ A tree widget specialised for displaying a JSON.
    """
    def __init__(self, roxxorEditorJSONwidget: RoxxorEditorJSON):
        """ Initialization of the object.

        Keyword arguments:
            roxxorEditorJSONwidget -- The roxxor editor JSON widget associated.           
        """
        QtGui.QTreeWidget.__init__(self)
        self.setHeaderHidden(True)
        self.setAlternatingRowColors(True)
        # Roxxor editor JSON widget
        self.roxxorEditorJSON = roxxorEditorJSONwidget
        # Root item
        self.rootItem = TreeWidgetItemJSON("root")
        self.insertTopLevelItem(0, self.rootItem)
        # Manage custom context menu
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.connect(self,
                     QtCore.SIGNAL('customContextMenuRequested(QPoint)'),
                     self.contextMenu)


    def loadData(self, data, parent: TreeWidgetItemJSON, force_explore=None):
        """ Load data from a list or a dictionary into the TreeWidget.

        Keyword arguments:
            data          -- The data to load in the tree.
            parent        -- The parent of the current item.
            force_explore -- Not None if the current item has to be explored.
        """
        if type(data) == str or type(data) == int or type(data) == bool or data == None:
            item = TreeWidgetItemJSON(data)
            parent.addChild(item)
            if force_explore:
                self.loadData(force_explore[data], item)
        elif type(data) == list:
            parent.dataType = list
            parent.setText()
            for i in range(len(data)):
                if type(data[i]) == dict or type(data[i]) == list:
                    self.loadData(i, parent, data)
                else:
                    self.loadData(i, parent)
        elif type(data) == dict:
            parent.dataType = dict
            parent.setText()
            for key in data.keys():
                if type(data[key]) == dict:
                    newParent = TreeWidgetItemJSON(key, dict)
                    parent.addChild(newParent)
                    self.loadData(data[key], newParent)
                elif type(data[key]) == list:
                    newParent = TreeWidgetItemJSON(key, list)
                    parent.addChild(newParent)
                    self.loadData(data[key], newParent)
                else:
                    self.loadData(key, parent)
        else:
            raise TypeError

    def recreateTreeView(self, data):
        """ Destroy the old tree and rebuild it from data in parameter.

        Keyword arguments:
            data -- The data structure to fill the tree with.
        """
        # "Destroy" old root and create a new one
        self.takeTopLevelItem(0)
        self.rootItem = TreeWidgetItemJSON("root")
        self.insertTopLevelItem(0, self.rootItem)
        # Load data into the tree and sort it
        self.loadData(data, self.rootItem)
        self.sortItems(0,0)
        self.rootItem.setExpanded(True)

    def getTreePath(self, item: QtGui.QTreeWidgetItem):
        """ Return the list of ancestors of the item passed in parameters
            (itself included) sorted in ascending order.

        Keyword arguments:
            item -- The item to get the path.
        """
        path = [item.data]
        parent = item.parent()
        if parent != None:
            path.insert(0, parent.data)
        while parent != None:
            parent = parent.parent()
            if parent != None:
                path.insert(0, parent.data)
        path.pop(0)
        return path

    def isLeaf(self, item: QtGui.QTreeWidgetItem):
        """ Return True if the item is a leaf of the QTreeWidget else
            return False.

        Keyword arguments:
            item -- The tree item to test.
        """
        return item.childCount() == 0

    def contextMenu(self, qPoint):
        """ Definition of the contextual menu of the tree view.

        Keyword arguments:
            qPoint -- The position of the mouse when the user clicked.
        """
        addKey = QtGui.QAction("Add value", self)
        addKey.triggered.connect(self.addKey)
        addList = QtGui.QAction("Add list", self)
        addList.triggered.connect(self.addList)
        addDict = QtGui.QAction("Add dictionary", self)
        addDict.triggered.connect(self.addDictionary)
        remove = QtGui.QAction("Remove", self)
        remove.triggered.connect(self.remove)
        createDict = QtGui.QAction("Create dictionary", self)
        createDict.triggered.connect(self.createDictOnRoot)
        createList = QtGui.QAction("Create list", self)
        createList.triggered.connect(self.createListOnRoot)
        menu = QtGui.QMenu(self)
        treeItem = self.selectedItems()[0]
        if treeItem.data != "root":
            if treeItem.dataType == None:
                menu.addAction(remove)
            else:
                if treeItem.dataType == list:
                    menu.addAction(addKey)
                    menu.addAction(addList)
                    menu.addAction(addDict)
                    menu.addAction(remove)
                elif treeItem.dataType == dict:
                    menu.addAction(addKey)
                    menu.addAction(addList)
                    menu.addAction(addDict)
                    menu.addAction(remove)
        else:
            if treeItem.childCount() == 0 and treeItem.dataType == None:
                menu.addAction(createList)
                menu.addAction(createDict)
            elif treeItem.dataType == list:
                menu.addAction(addKey)
                menu.addAction(addList)
                menu.addAction(addDict)
                menu.addAction(remove)
            elif treeItem.dataType == dict:
                menu.addAction(addKey)
                menu.addAction(addList)
                menu.addAction(addDict)
                menu.addAction(remove)
        menu.exec_(QtGui.QCursor.pos())


    def addKey(self):
        """ Add a key in the data structure selected by the user in
            the tree view.
        """
        item = self.selectedItems()[0]
        path = self.getTreePath(item)
        originalDataStruct = self.roxxorEditorJSON.extractDataStructure(
                                    self.roxxorEditorJSON.originalData, path)
        dataStruct = self.roxxorEditorJSON.extractDataStructure(
                                    self.roxxorEditorJSON.data, path)
        if type(dataStruct) == list:
            index, ok = askForIndex(0, len(dataStruct))
            if ok:
                data, ok = askForData()
                if ok:
                    originalDataStruct.insert(index, data)
                    dataStruct.insert(index, data)
        elif type(dataStruct) == dict:
            keyName, ok = askForKey()
            if ok:
                data, ok = askForData()
                if ok:
                    originalDataStruct[keyName] = data
                    dataStruct[keyName] = data
        self.recreateTreeView(self.roxxorEditorJSON.data)

    def addDictionary(self):
        """ Add a dictionary in the data structure selected by the user in
            the tree view.
        """
        item = self.selectedItems()[0]
        path = self.getTreePath(item)
        originalDataStruct = self.roxxorEditorJSON.extractDataStructure(
                                    self.roxxorEditorJSON.originalData, path)
        dataStruct = self.roxxorEditorJSON.extractDataStructure(
                                    self.roxxorEditorJSON.data, path)
        if type(dataStruct) == list:
            index, ok = askForIndex(0, len(dataStruct))
            if ok:
                originalDataStruct.insert(index, dict())
                dataStruct.insert(index, dict())
        elif type(dataStruct) == dict:
            keyName, ok = askForKey()
            if ok:
                originalDataStruct[keyName] = dict()
                dataStruct[keyName] = dict()
        self.recreateTreeView(self.roxxorEditorJSON.data)


    def addList(self):
        """ Add a list in the data structure selected by the user in
            the tree view.
        """
        item = self.selectedItems()[0]
        path = self.getTreePath(item)
        originalDataStruct = self.roxxorEditorJSON.extractDataStructure(
                                    self.roxxorEditorJSON.originalData, path)
        dataStruct = self.roxxorEditorJSON.extractDataStructure(
                                    self.roxxorEditorJSON.data, path)
        if type(dataStruct) == list:
            index, ok = askForIndex(0, len(dataStruct))
            if ok:
                originalDataStruct.insert(index, list())
                dataStruct.insert(index, list())
        elif type(dataStruct) == dict:
            keyName, ok = askForKey()
            if ok:
                originalDataStruct[keyName] = list()
                dataStruct[keyName] = list()
        self.recreateTreeView(self.roxxorEditorJSON.data)

    def remove(self):
        """ Remove the data represented by the item user clicked on.
        """
        if isConfirmed("Are you sure to delete this item?"):
            item = self.selectedItems()[0]
            path = self.getTreePath(item)
            endPath = path[len(path)-1]
            path = path[0:len(path)-1]
            dataStruct = self.roxxorEditorJSON.extractDataStructure(
                                    self.roxxorEditorJSON.data,path)
            if type(endPath) == int:
                dataStruct.pop(endPath)
            else:
                del(dataStruct[endPath])
            self.roxxorEditorJSON.originalData = copy.deepcopy(self.roxxorEditorJSON.data)
            self.recreateTreeView(self.roxxorEditorJSON.data)
            self.roxxorEditorJSON.key = None
            self.roxxorEditorJSON.keyLabel.hide()
            self.roxxorEditorJSON.textField.hide()
            self.roxxorEditorJSON.valueLabel.hide()
            self.roxxorEditorJSON.modificationsButton.hide()

    def createDictOnRoot(self):
        """ Create a dictionary on the "root" of the JSON.
        """
        self.roxxorEditorJSON.data = {}
        self.roxxorEditorJSON.originalData = {}
        self.recreateTreeView(self.roxxorEditorJSON.data)

    def createListOnRoot(self):
        """ Create an array on the "root" of the JSON.
        """
        self.roxxorEditorJSON.data = []
        self.roxxorEditorJSON.originalData = []
        self.recreateTreeView(self.roxxorEditorJSON.data)

class DataDialog(QtGui.QMessageBox):
    """ This class is a dialog for asking the user a data in a text text field
        and its type.
    """
    def __init__(self, parent=None):
        """ Initialization of the object.
        """
        QtGui.QMessageBox.__init__(self, parent)
        self.setWindowTitle("Data")
        self.setText("Enter the data:")
        self.setStandardButtons(QtGui.QMessageBox.Cancel | QtGui.QMessageBox.Ok)
        self.setDefaultButton(QtGui.QMessageBox.Cancel)
        # Radio buttons
        self.radioButtonNull = QtGui.QRadioButton()
        self.radioButtonNull.setText("null")
        self.radioButtonInteger = QtGui.QRadioButton()
        self.radioButtonInteger.setText("Integer")
        self.radioButtonFloat = QtGui.QRadioButton()
        self.radioButtonFloat.setText("Float")
        self.radioButtonString = QtGui.QRadioButton()
        self.radioButtonString.setText("String")
        self.radioButtonString.setChecked(True)
        self.radioButtonBoolean = QtGui.QRadioButton()
        self.radioButtonBoolean.setText("Boolean")
        # Button group
        buttonGroup = QtGui.QButtonGroup()
        buttonGroup.addButton(self.radioButtonNull, 1)
        buttonGroup.addButton(self.radioButtonInteger, 2)
        buttonGroup.addButton(self.radioButtonFloat, 3)
        buttonGroup.addButton(self.radioButtonString, 4)
        buttonGroup.addButton(self.radioButtonBoolean, 5)
        # Text field
        self.textField = QtGui.QTextEdit() 

        # Layout management
        layout = self.layout()
        vlayout = QtGui.QVBoxLayout()
        vlayout.addWidget(self.radioButtonNull)
        vlayout.addWidget(self.radioButtonInteger)
        vlayout.addWidget(self.radioButtonFloat)
        vlayout.addWidget(self.radioButtonString)
        vlayout.addWidget(self.radioButtonBoolean)
        layout.addLayout(vlayout, 1, 2)
        layout.addWidget(self.textField, 1, 1)

    def typeChecked(self):
        """ Return the python class that represent the type choosed by
            the user.
        """
        if self.radioButtonNull.isChecked():
            return None
        elif self.radioButtonInteger.isChecked():
            return int
        elif self.radioButtonFloat.isChecked():
            return float
        elif self.radioButtonString.isChecked():
            return str
        else:
            return bool

    def exec_(self, *args, **kwargs):
        """ Override the exec_ method return a boolean, the class that
            represent the type checked or None if null were checked and
            the data typed by the user as a string. The boolean is True
            if the button "Ok" were pressed else it return False.
        """
        result = QtGui.QMessageBox.exec_(self, *args, **kwargs)
        return result == QtGui.QMessageBox.Ok, self.typeChecked(), self.textField.toPlainText()
