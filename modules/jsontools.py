#!/bin/python3
# -*- coding: utf-8 -*-

import json
import copy
from roxxoreditorwidget import *

def registerModule(modulesDict):
    modulesDict['.json'] = RoxxorEditorJSON


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
        self.treeWidget = QtGui.QTreeWidget()
        self.treeWidget.setHeaderHidden(True)
        self.treeWidget.setAlternatingRowColors(True)
        self.rootItem = QtGui.QTreeWidgetItem()
        self.rootItem.setData(0, 0, "root")
        self.treeWidget.insertTopLevelItem(0, self.rootItem)
        self.connect(self.treeWidget,
                     QtCore.SIGNAL("itemClicked(QTreeWidgetItem*, int)"),
                     self.onClickItem)

        # Action on tree widget
        addKey = QtGui.QAction("Add value", self)
        # addKey.triggered.connect() TODO
        addList = QtGui.QAction("Add list", self)
        # addList.triggered.connect() TODO
        addDict = QtGui.QAction("Add dictionary", self)
        # addDict.triggered.connect() TODO
        editKey = QtGui.QAction("Edit", self)
        # editKey.triggered.connect() TODO
        remove = QtGui.QAction("Remove", self)
        # remove.triggered.connect() TODO

        self.treeWidget.addAction(addKey)
        self.treeWidget.addAction(addList)
        self.treeWidget.addAction(addDict)
        self.treeWidget.addAction(editKey)
        self.treeWidget.addAction(remove)
        self.treeWidget.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)

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
        if self.path and self.key != None:
            self.saveValue()
        if self.data and self.isLeaf(item):
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
            self.keyLabel.show()
            self.valueLabel.show()
            self.textField.show()
            self.modificationsButton.show()
        else:
            # Key Label
            self.keyLabel.setText(KEY_LABEL_DEFAULT)

            # Update path
            self.path = self.getTreePath(item)
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

    # def addButtonClicked(self):
    #     """ Action performed when the add button is clicked
    #     """
    #     dataStruct = self.data
    #     for i in range(len(self.path)-1):
    #         try:
    #             j = int(self.path[i])
    #             dataStruct = dataStruct[j]
    #         except ValueError:
    #             dataStruct = dataStruct[self.path[i]]
    #     self.key = self.keyTextField.text()
    #     data = self.textField.toPlainText()
    #     if self.key != "":
    #         if type(dataStruct) == list:
    #             try:
    #                 i = int(self.key)
    #                 dataStruct[i] = data
    #             except ValueError:
    #                 errorDialog("The index must be an integer!")
    #         elif type(dataStruct) == dict:
    #             dataStruct[self.key] = data

    #         for i in range(self.rootItem.childCount()):
    #             self.rootItem.removeChild(self.rootItem.child(i))

    #         self.setData(self.data)
    #     else:
    #         errorDialog("A key can't be empty!")

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

    def isLeaf(self, item: QtGui.QTreeWidgetItem):
        """ Return True if the item is a leaf of the QTreeWidget else
            return False.
        """
        return item.childCount() == 0

    def setData(self, filename):
        """ Set the instance variable self.data and refresh the tree view.
        """
        self.originalData = self.read(filename)
        self.data = copy.deepcopy(self.originalData)
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
