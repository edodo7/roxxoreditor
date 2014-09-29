#!/bin/python3
# -*- coding: utf-8 -*-
""" This module contains stuff concerning the popups, dialog, ... """

from PyQt4 import QtGui

def aboutDialog():
    """ Create and display the about dialog about Roxxor Editor.
    """
    aboutTitle = 'About Roxxor Editor'
    aboutContent = 'The awesome structured files editor.\n\n'
    aboutContent += 'By Julien Delplanque and Alexandre Devaux'

    QtGui.QMessageBox.information(None, aboutTitle, aboutContent)

def errorDialog(errorContent):
    """ Create and display an error dialog with the specified content.

    Keyword arguments:
        errorContent -- The str contening the error explanation to display.
    """
    QtGui.QMessageBox.warning(None, 'Error', errorContent)

def askForKey():
    """ Create and display a dialog that ask to the user the key name.
    """
    key, ok = QtGui.QInputDialog.getText(None, 'Key name', 
            'Enter the key name:')
    # TODO manage ok
    return key

def askForIndex(minimum: int, maximum: int):
    """ Create and display a dialog that ask to the user an index.
    """
    index, ok = QtGui.QInputDialog.getInteger(None, 'Key name', 
            'Enter the index:', min=minimum, max=maximum)
    # TODO manage ok
    return index
