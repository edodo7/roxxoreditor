#!/usr/bin/python3
# -*- coding: utf-8 -*-
""" This module contains stuff concerning the popups, dialog, ... """

# System
from PyQt4 import QtGui

# Core
from core.tools import loadLangFile

LANG = loadLangFile("core/lang.json")

def aboutDialog(parent: QtGui.QWidget):
    """ Create and display the about dialog about Roxxor Editor.
    """
    aboutTitle = 'About RoxxoR Editor\n===================\n'
    aboutContent = 'The awesome structured files editor,\n'
    aboutContent += 'by Julien Delplanque and Alexandre Devaux.'

    QtGui.QMessageBox.information(parent, aboutTitle, aboutContent)

def errorDialog(parent: QtGui.QWidget, errorContent: str):
    """ Create and display an error dialog with the specified content.

    Keyword arguments:
        errorContent -- The str contening the error explanation to display.
    """
    QtGui.QMessageBox.warning(parent, 'Error', errorContent)

def modulesDialog(parent: QtGui.QWidget, modulesList: list):
    """ Create and display a combobox with all usables modules, to use with
        the selected file. But the file extension doesn't exist or isn't known
        by the editor. The user can select manually in the list the module to
        process the file. The function return the choice of the user.

    Keyword arguments:
        modulesList -- The list of modules name.
    """
    modulesList = list(map(lambda moduleExt: moduleExt[1:].upper(), modulesList))
    modulesList.sort()
    ext, proceed = QtGui.QInputDialog.getItem(parent, 'Module selecter',
                               'The extension of the file isn\'t known by ' +
                               'Roxxor Editor.\nChoose the module to use ' +
                               'with the file :', modulesList, editable=False)
    if proceed:
        return '.' + ext.lower()

def saveDialog(parent: QtGui.QWidget):
    """
    """
    reply = QtGui.QMessageBox.question(parent, 'Save before quitting?',
                                    "Do you want to save before quitting?",
                                    QtGui.QMessageBox.Yes | QtGui.QMessageBox.No,
                                    QtGui.QMessageBox.Yes)
    if reply == QtGui.QMessageBox.Yes:
        return True
    else:
        return False

def preferencesDialog(parent: QtGui.QWidget, languageList: list):
    """
    """
    return QtGui.QInputDialog.getItem(parent, "Preferences",
                                    "Choose your language:",
                                    languageList, editable=False)
