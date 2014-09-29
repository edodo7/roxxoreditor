#!/bin/python3
# -*- coding: utf-8 -*-

import json
import copy
from roxxoreditorwidget import *
from dialog import *

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
    data, ok = QtGui.QInputDialog.getText(None, 'Data', 
            'Enter the data:')
    return data, ok

def askForIndex(minimum: int, maximum: int):
    """ Create and display a dialog that ask to the user an index.
    """
    index, ok = QtGui.QInputDialog.getInteger(None, 'Index', 
            'Enter the index:', value=maximum, min=minimum, max=maximum)
    return index, ok

def isConfirmed():
    """
    """
    reply = QtGui.QMessageBox.question(None, 'Message',
                            "Are you sure to delete this item?",
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

    def extractDataStructure(self, dataStruct, path):
        """ Extract the sub data structure defined by the path from dataStruct.
        """
        for i in range(len(path)):
            try:
                j = int(path[i])
                dataStruct = dataStruct[j]
            except ValueError:
                dataStruct = dataStruct[path[i].split(" ")[0]]
        return dataStruct

    def onClickItem(self, item: QtGui.QTreeWidgetItem, i):
        """ Action performed when an item in the QTreeWidget is clicked.
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
            self.pathLabel.setText("/"+'>'.join(self.path))
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
            self.pathLabel.setText("/"+'>'.join(self.path))

            self.keyLabel.hide()
            self.valueLabel.hide()
            self.textField.hide()
            self.modificationsButton.hide()

            self.key = None

    def restoreButtonClicked(self):
        """ Action performed when the restore button is clicked.
        """
        dataStruct = self.originalData
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
            errorDialog("Wrong entry!")

    def setData(self, filename):
        """ Set the instance variable self.data and refresh the tree view.
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
        """
        """
        QtGui.QTreeWidgetItem.__init__(self)
        self.data = data
        self.dataType = dataType
        self.setText()

    def setText(self):
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
        """
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


    def loadData(self, data, parent, force_explore=None):
        """ Load data from a list or a dictionary into the TreeWidget.
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
        """
        path = [str(item.data)]
        parent = item.parent()
        if parent != None:
            path.insert(0, str(parent.data))
        while parent != None:
            parent = parent.parent()
            if parent != None:
                path.insert(0, str(parent.data))
        path.pop(0)
        return path

    def isLeaf(self, item: QtGui.QTreeWidgetItem):
        """ Return True if the item is a leaf of the QTreeWidget else
            return False.
        """
        return item.childCount() == 0

    def contextMenu(self, qPoint):
        """ Definition of the contextual menu of the tree view.
        """
        addKey = QtGui.QAction("Add value", self)
        addKey.triggered.connect(self.addKey)
        addList = QtGui.QAction("Add list", self)
        addList.triggered.connect(self.addList)
        addDict = QtGui.QAction("Add dictionary", self)
        addDict.triggered.connect(self.addDictionary)
        remove = QtGui.QAction("Remove", self)
        remove.triggered.connect(self.remove)
        menu = QtGui.QMenu(self)
        treeItem = self.selectedItems()[0]
        if treeItem.text(0) != "root":
            labelSplitted = treeItem.text(0).split()
            if len(labelSplitted) == 1:
                menu.addAction(remove)
            else:
                if labelSplitted[1] == "[]":
                    menu.addAction(addKey)
                    menu.addAction(addList)
                    menu.addAction(addDict)
                    menu.addAction(remove)
                elif labelSplitted[1] == "{}":
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
        if isConfirmed():
            item = self.selectedItems()[0]
            path = self.getTreePath(item)
            dataStruct = self.roxxorEditorJSON.data
            for i in range(len(path)-1):
                try:
                    j = int(path[i])
                    dataStruct = dataStruct[j]
                except ValueError:
                    dataStruct = dataStruct[path[i]]
            try:
                j = int(path[len(path)-1])
                dataStruct.pop(j)
            except ValueError:
                del(dataStruct[path[len(path)-1]])
            self.recreateTreeView(self.roxxorEditorJSON.data)
