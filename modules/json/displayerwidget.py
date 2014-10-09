#!/usr/bin/python3
# -*- coding: utf-8 -*-

# System
import copy

from PyQt4 import QtCore
from PyQt4 import QtGui

# Core
from core.dialog import *
from core.tools import loadLangFile
from core.tools import loadRoxxorRc

# Modules JSON
from modules.json.dialogs import *
from modules.json.tools import extractDataStructure

# CONSTANTS
LANG = loadLangFile("modules/json/lang.json")[loadRoxxorRc()["language"]]

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

    def getChildWithKey(self, key):
        """ Return the child wich its data is equal to the key. If no child
            statisfy the key, a KeyError is raised.

        Keyword arguments:
            key -- The key you want to find the child.
        """
        for i in range(self.childCount()):
            if self.child(i).data == key:
                return self.child(i)
        raise KeyError()

    def deepCopy(self):
        """ Make a deep copy of the TreeWidgetItemJSON and return it.
        """
        def deepCopyRec(newParent, oldNode):
            newNode = TreeWidgetItemJSON(oldNode.data, oldNode.dataType)
            for i in range(oldNode.childCount()):
                deepCopyRec(newNode, oldNode.child(i))
            if newParent != None:
                newParent.addChild(newNode)
                return newParent
            else:
                return newNode

        return deepCopyRec(None, self)

class TreeWidgetJSON(QtGui.QTreeWidget):
    """ A tree widget specialised for displaying a JSON.
    """
    def __init__(self, roxxorEditorJSONwidget):
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
        # Manage custom context menu
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.connect(self,
                     QtCore.SIGNAL('customContextMenuRequested(QPoint)'),
                     self.contextMenu)
        # Copy variables
        self.nodeCopiedBuffer = None
        self.dataCopiedBuffer = None


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
        self.recreateEmptyTreeView()
        # Load data into the tree and sort it
        self.loadData(data, self.rootItem)
        self.sortItems(0,0)
        self.rootItem.setExpanded(True)

    def recreateEmptyTreeView(self):
        """ Destroy the old tree and rebuild an empty one.
        """
        # "Destroy" old root and create a new one
        self.takeTopLevelItem(0)
        self.rootItem = TreeWidgetItemJSON("root")
        self.insertTopLevelItem(0, self.rootItem)

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

    def getNode(self, path: list):
        """ Return the node located by the path from the tree.

        Keyword arguments:
            path -- the location of the node.
        """
        item = self.rootItem
        for key in path:
            item = item.getChildWithKey(key)
        return item

    def isLeaf(self, item: QtGui.QTreeWidgetItem):
        """ Return True if the item is a leaf of the QTreeWidget else
            return False.

        Keyword arguments:
            item -- The tree item to test.
        """
        return item.childCount() == 0

    def addNode(self, path: list, node: TreeWidgetItemJSON):
        """ Add the TreeWidgetItemJSON to the child located at path.

        Keyword arguments:
            path -- The path were to add the node.
            node -- The node to add.
        """
        item = self.getNode(path)
        if item.dataType == list and node.dataType != list and node.dataType != dict:
            item.addChild(TreeWidgetItemJSON(item.childCount(), int))
        else:
            item.addChild(node)

    def copyNode(self, path: list):
        """ Copy the node located by the path in self.nodeCopiedBuffer.

        Keyword arguments:
            path -- The path were is located the node.
        """
        node = self.getNode(path)
        self.nodeCopiedBuffer = node.deepCopy()#(node.data, node.dataType)

    def editNode(self, path: list, newKeyName: str):
        """ Edit the name of the key for the node located by the path.

        Keyword arguments:
            path       -- The path of the node to modify.
            newKeyName -- The new key name.
        """
        item = self.getNode(path)
        item.data = newKeyName
        item.setText()

    def removeNode(self, path: list):
        """ Remove the node located by the path.

        Keyword arguments:
            path -- The path to the node to remove as a list.
        """
        item = self.getNode(path[0:len(path)-1])
        if item.dataType == list:
            item.removeChild(item.child(item.childCount()-1))
        else:
            childToRemove = None
            for i in range(item.childCount()):
                if item.child(i).data == path[len(path)-1]:
                    childToRemove = item.child(i)
                    break
            item.removeChild(childToRemove)

    def contextMenu(self, qPoint):
        """ Definition of the contextual menu of the tree view.

        Keyword arguments:
            qPoint -- The position of the mouse when the user clicked.
        """
        if len(self.selectedItems()) > 0:
            addKey = QtGui.QAction(LANG["addKeyAction"], self)
            addKey.triggered.connect(self.addKey)
            addList = QtGui.QAction(LANG["addListAction"], self)
            addList.triggered.connect(self.addList)
            addDict = QtGui.QAction(LANG["addDictAction"], self)
            addDict.triggered.connect(self.addDictionary)
            remove = QtGui.QAction(LANG["removeAction"], self)
            remove.triggered.connect(self.remove)
            createDict = QtGui.QAction(LANG["createDictAction"], self)
            createDict.triggered.connect(self.createDictOnRoot)
            createList = QtGui.QAction(LANG["createListAction"], self)
            createList.triggered.connect(self.createListOnRoot)
            editKey = QtGui.QAction(LANG["editKeyAction"], self)
            editKey.triggered.connect(self.editKey)
            copy = QtGui.QAction(LANG["copyAction"], self)
            copy.triggered.connect(self.copy)
            paste = QtGui.QAction(LANG["pasteAction"], self)
            paste.triggered.connect(self.paste)
            patternCopy = QtGui.QAction(LANG["patternCopyAction"], self)
            menu = QtGui.QMenu(self)
            treeItem = self.selectedItems()[0]
            if treeItem.data != "root":
                if treeItem.parent().dataType == dict:
                    menu.addAction(editKey)
                if treeItem.dataType == list:
                    menu.addAction(addKey)
                    menu.addAction(addList)
                    menu.addAction(addDict)
                    menu.addAction(copy)
                    if self.dataCopiedBuffer != None:
                        menu.addAction(paste)
                    menu.addAction(patternCopy)
                    menu.addAction(remove)
                elif treeItem.dataType == dict:
                    menu.addAction(addKey)
                    menu.addAction(addList)
                    menu.addAction(addDict)
                    menu.addAction(copy)
                    if self.dataCopiedBuffer != None:
                        menu.addAction(paste)
                    menu.addAction(patternCopy)
                    menu.addAction(remove)
                else:
                    menu.addAction(copy)
                    menu.addAction(remove)
            else:
                if treeItem.childCount() == 0 and treeItem.dataType == None:
                    menu.addAction(createList)
                    menu.addAction(createDict)
                elif treeItem.dataType == list:
                    menu.addAction(addKey)
                    menu.addAction(addList)
                    menu.addAction(addDict)
                    menu.addAction(copy)
                    if self.dataCopiedBuffer != None:
                        menu.addAction(paste)
                    menu.addAction(patternCopy)
                elif treeItem.dataType == dict:
                    menu.addAction(addKey)
                    menu.addAction(addList)
                    menu.addAction(addDict)
                    menu.addAction(copy)
                    if self.dataCopiedBuffer != None:
                        menu.addAction(paste)
                    menu.addAction(patternCopy)
            menu.exec_(QtGui.QCursor.pos())

    def addKey(self):
        """ Add a key in the data structure selected by the user in
            the tree view.
        """
        item = self.selectedItems()[0]
        path = self.getTreePath(item)
        originalDataStruct = extractDataStructure(
                                    self.roxxorEditorJSON.originalData, path)
        dataStruct = extractDataStructure(self.roxxorEditorJSON.data, path)
        if type(dataStruct) == list:
            index, ok = askForIndex(self, 0, len(dataStruct))
            if ok:
                data, ok = askForData(self)
                if ok:
                    originalDataStruct.insert(index, data)
                    dataStruct.insert(index, data)
                    newItem = TreeWidgetItemJSON(index, type(data))
                    self.addNode(path, newItem)
                    newItem.setExpanded(True)
        elif type(dataStruct) == dict:
            keyName, ok = askForKey(self)
            if ok and keyName != "":
                data, ok = askForData(self)
                if ok:
                    originalDataStruct[keyName] = data
                    dataStruct[keyName] = data
                    newItem = TreeWidgetItemJSON(keyName, type(data))
                    self.addNode(path, newItem)
                    newItem.setExpanded(True)
            elif ok and keyName == "":
                errorDialog(self, LANG["errorKeyCanNotEmpty"])

    def addDictionary(self):
        """ Add a dictionary in the data structure selected by the user in
            the tree view.
        """
        item = self.selectedItems()[0]
        path = self.getTreePath(item)
        originalDataStruct = extractDataStructure(
                                    self.roxxorEditorJSON.originalData, path)
        dataStruct = extractDataStructure(self.roxxorEditorJSON.data, path)
        if type(dataStruct) == list:
            index, ok = askForIndex(self, 0, len(dataStruct))
            if ok:
                originalDataStruct.insert(index, dict())
                dataStruct.insert(index, dict())
                newItem = TreeWidgetItemJSON(index, dict)
                self.addNode(path, newItem)
                newItem.setExpanded(True)
        elif type(dataStruct) == dict:
            keyName, ok = askForKey(self)
            if ok and keyName != "":
                originalDataStruct[keyName] = dict()
                dataStruct[keyName] = dict()
                newItem = TreeWidgetItemJSON(keyName, dict)
                self.addNode(path, newItem)
                newItem.setExpanded(True)
            elif ok and keyName == "":
                errorDialog(self, LANG["errorKeyCanNotEmpty"])


    def addList(self):
        """ Add a list in the data structure selected by the user in
            the tree view.
        """
        item = self.selectedItems()[0]
        path = self.getTreePath(item)
        originalDataStruct = extractDataStructure(
                                    self.roxxorEditorJSON.originalData, path)
        dataStruct = extractDataStructure(self.roxxorEditorJSON.data, path)
        if type(dataStruct) == list:
            index, ok = askForIndex(self, 0, len(dataStruct))
            if ok:
                originalDataStruct.insert(index, list())
                dataStruct.insert(index, list())
                newItem = TreeWidgetItemJSON(index, list)
                self.addNode(path, newItem)
                newItem.setExpanded(True)
        elif type(dataStruct) == dict:
            keyName, ok = askForKey(self)
            if ok and keyName != "":
                originalDataStruct[keyName] = list()
                dataStruct[keyName] = list()
                newItem = TreeWidgetItemJSON(keyName, list)
                self.addNode(path, newItem)
                newItem.setExpanded(True)
            elif ok and keyName == "":
                errorDialog(self, LANG["errorKeyCanNotEmpty"])

    def remove(self):
        """ Remove the data represented by the item user clicked on.
        """
        if isConfirmed(self, "Are you sure to delete this item?"):
            item = self.selectedItems()[0]
            path = self.getTreePath(item)
            endPath = path[len(path)-1]
            path = path[0:len(path)-1]
            dataStruct = extractDataStructure(self.roxxorEditorJSON.data,path)
            if type(endPath) == int:
                dataStruct.pop(endPath)
            else:
                del(dataStruct[endPath])
            self.roxxorEditorJSON.originalData = copy.deepcopy(self.roxxorEditorJSON.data)
            self.removeNode(path+[endPath])
            self.roxxorEditorJSON.key = None
            self.roxxorEditorJSON.keyLabel.hide()
            self.roxxorEditorJSON.currentInputWidget().hide()
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

    def editKey(self):
        """ Edit the key selected by the user.
        """
        item = self.selectedItems()[0]
        path = self.getTreePath(item)
        subPath = path[0:len(path)-1]
        index = path[len(path)-1]
        originalDataStruct = extractDataStructure(self.roxxorEditorJSON.originalData, subPath)
        dataStruct = extractDataStructure(self.roxxorEditorJSON.data, subPath)
        newKey, ok = askForKey(self)
        if ok and newKey != "":
            originalData = originalDataStruct[index]
            data = dataStruct[index]
            del(originalDataStruct[index])
            del(dataStruct[index])
            originalDataStruct[newKey] = originalData
            dataStruct[newKey] = data
            self.editNode(path, newKey)
            self.roxxorEditorJSON.key = None
            self.roxxorEditorJSON.keyLabel.hide()
            self.roxxorEditorJSON.currentInputWidget().hide()
            self.roxxorEditorJSON.valueLabel.hide()
            self.roxxorEditorJSON.modificationsButton.hide()
        elif ok and newKey == "":
            errorDialog(self, LANG["errorKeyCanNotEmpty"])

    def copy(self):
        """ Copy the data selected by the user into the copy buffer.
        """
        item = self.selectedItems()[0]
        path = self.getTreePath(item)
        subPath = path[0:len(path)-1]
        key = path[len(path)-1]
        dataStruct = extractDataStructure(self.roxxorEditorJSON.data, subPath)
        self.dataCopiedBuffer = (key, dataStruct[key])
        self.copyNode(path)

    def paste(self):
        """ Paste the data precedently copied by the user in the data structure
            selected.
        """
        item = self.selectedItems()[0]
        path = self.getTreePath(item)
        subPath = path[0:len(path)-1]
        dataStruct = extractDataStructure(self.roxxorEditorJSON.data, path)
        originalDataStruct = extractDataStructure(
                                    self.roxxorEditorJSON.originalData, path)
        if type(dataStruct) == dict:
            key, ok = askForKey(self)
            if ok:
                originalDataStruct[key] = self.dataCopiedBuffer[1]
                dataStruct[key] = self.dataCopiedBuffer[1]
                self.nodeCopiedBuffer.data = key
                self.nodeCopiedBuffer.setText()
                self.addNode(path, self.nodeCopiedBuffer)
                self.nodeCopiedBuffer.setExpanded(True)
                self.nodeCopiedBuffer = None
                self.sortItems(0,0)
        else:
            index, ok = askForIndex(self, 0, item.childCount())
            if ok:
                originalDataStruct.insert(index, self.dataCopiedBuffer[1])
                dataStruct.insert(index, self.dataCopiedBuffer[1])
                self.nodeCopiedBuffer.data = index
                self.nodeCopiedBuffer.setText()
                self.addNode(path, self.nodeCopiedBuffer)
                self.nodeCopiedBuffer.setExpanded(True)
                self.nodeCopiedBuffer = None
                self.sortItems(0,0)

    def patternCopy(self):
        """ Copy the pattern extracted from the data structure selected by the
            user into the patterCopy buffer.
        """
        pass

    def patternPaste(self):
        """ Paste the pattern precedently copied byt the user in the data
            structure selected.
        """
        pass
