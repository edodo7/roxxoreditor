#!/bin/python3
# -*- coding: utf-8 -*-

from PyQt4 import QtGui

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
