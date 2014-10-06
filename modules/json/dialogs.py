#!/usr/bin/python3
# -*- coding: utf-8 -*-

# System
from PyQt4 import QtGui
from PyQt4 import QtCore

from core.dialog import *

def askForKey(parent: QtGui.QWidget):
    """ Create and display a dialog that ask to the user the key name.
    """
    key, ok = QtGui.QInputDialog.getText(parent, 'Key name',
            'Enter the key name:')
    return key, ok

def askForData(parent: QtGui.QWidget):
    """ Create and display a dialog that ask to the user the data.
    """
    ok, dataType, data = DataDialog(parent).exec_()
    if dataType == None:
        data = None
    elif dataType == bool:
        if data == 'True':
            data = True
        else:
            data = False
    else:
        try:
            data = dataType(data)
        except ValueError:
            errorDialog(parent, "The data typed does not correspond to the type choosen.")
            ok = False
    return data, ok

def askForIndex(parent: QtGui.QWidget, minimum: int, maximum: int):
    """ Create and display a dialog that ask to the user an index.

    Keyword arguments:
        minimum -- Lower boundary of the index choice.
        maximum -- Higher boundary of the index choice.
    """
    index, ok = QtGui.QInputDialog.getInteger(parent, 'Index',
            'Enter the index:', value=maximum, min=minimum, max=maximum)
    return index, ok

def isConfirmed(parent: QtGui.QWidget, description: str):
    """ Create and display a dialog that ask to the user if he confirm
        the action described in the string in parameter.

    Keyword arguments:
        description -- The description of what have to be confirmed.
    """
    reply = QtGui.QMessageBox.question(parent, 'Confirmation',
                            description,
                            QtGui.QMessageBox.Yes |
                            QtGui.QMessageBox.No, QtGui.QMessageBox.No)
    if reply == QtGui.QMessageBox.Yes:
        return True
    return False

class DataDialog(QtGui.QMessageBox):
    """ This class is a dialog for asking the user a data in a text text field
        and its type.
    """
    def __init__(self, parent: QtGui.QWidget):
        """ Initialization of the object.
        """
        QtGui.QMessageBox.__init__(self, parent)
        self.setWindowTitle("Data")
        self.setText("Enter the data:")
        self.setStandardButtons(QtGui.QMessageBox.Cancel | QtGui.QMessageBox.Ok)
        self.setDefaultButton(QtGui.QMessageBox.Cancel)
        # Input widget
        self.stringWidget = QtGui.QTextEdit()
        self.booleanWidget = QtGui.QComboBox(self)
        self.booleanWidget.setMaximumSize(QtCore.QSize(150,40))
        self.booleanWidget.addItem("True")
        self.booleanWidget.addItem("False")
        self.noneWidget = QtGui.QLabel("null")
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
        # Radio buttons
        self.radioButtonNull = QtGui.QRadioButton()
        self.radioButtonNull.setText("null")
        self.radioButtonNull.toggled.connect(self.radioNullClicked)
        self.radioButtonInteger = QtGui.QRadioButton()
        self.radioButtonInteger.setText("Integer")
        self.radioButtonInteger.toggled.connect(self.radioIntegerClicked)
        self.radioButtonFloat = QtGui.QRadioButton()
        self.radioButtonFloat.setText("Float")
        self.radioButtonFloat.toggled.connect(self.radioFloatClicked)
        self.radioButtonString = QtGui.QRadioButton()
        self.radioButtonString.setText("String")
        self.radioButtonString.toggled.connect(self.radioStringClicked)
        self.radioButtonString.setChecked(True)
        self.radioButtonBoolean = QtGui.QRadioButton()
        self.radioButtonBoolean.setText("Boolean")
        self.radioButtonBoolean.toggled.connect(self.radioBooleanClicked)
        # Button group
        buttonGroup = QtGui.QButtonGroup()
        buttonGroup.addButton(self.radioButtonNull, 1)
        buttonGroup.addButton(self.radioButtonInteger, 2)
        buttonGroup.addButton(self.radioButtonFloat, 3)
        buttonGroup.addButton(self.radioButtonString, 4)
        buttonGroup.addButton(self.radioButtonBoolean, 5)
        # Layout management
        layout = self.layout()
        vlayout = QtGui.QVBoxLayout()
        vlayout.addWidget(self.radioButtonNull)
        vlayout.addWidget(self.radioButtonInteger)
        vlayout.addWidget(self.radioButtonFloat)
        vlayout.addWidget(self.radioButtonString)
        vlayout.addWidget(self.radioButtonBoolean)
        layout.addLayout(vlayout, 1, 2)
        layout.addLayout(self.inputWidgetLayout, 1, 1)

    def radioNullClicked(self):
        """ Set the self.noneWidget on top of the QStackedLayout's stack.
        """
        self.inputWidgetLayout.setCurrentWidget(self.noneWidget)

    def radioIntegerClicked(self):
        """ Set the self.integerWidget on top of the QStackedLayout's stack.
        """
        self.inputWidgetLayout.setCurrentWidget(self.integerWidget)

    def radioFloatClicked(self):
        """ Set the self.floatWidget on top of the QStackedLayout's stack.
        """
        self.inputWidgetLayout.setCurrentWidget(self.floatWidget)

    def radioStringClicked(self):
        """ Set the self.stringWidget on top of the QStackedLayout's stack.
        """
        self.inputWidgetLayout.setCurrentWidget(self.stringWidget)

    def radioBooleanClicked(self):
        """ Set the self.booleanWidget on top of the QStackedLayout's stack.
        """
        self.inputWidgetLayout.setCurrentWidget(self.booleanWidget)


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

    def valueEntered(self):
        """ Return the value entered by the user according to widget
            corresponding to the type choosen by the user.
        """
        widget = self.inputWidgetLayout.currentWidget()
        if self.radioButtonNull.isChecked():
            return None
        elif self.radioButtonInteger.isChecked():
            return widget.text()
        elif self.radioButtonFloat.isChecked():
            return widget.text()
        elif self.radioButtonString.isChecked():
            return widget.toPlainText()
        else:
            return widget.currentText()

    def exec_(self, *args, **kwargs):
        """ Override the exec_ method return a boolean, the class that
            represent the type checked or None if null were checked and
            the data typed by the user as a string. The boolean is True
            if the button "Ok" were pressed else it return False.
        """
        result = QtGui.QMessageBox.exec_(self, *args, **kwargs)
        return result == QtGui.QMessageBox.Ok, self.typeChecked(), self.valueEntered()
