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
