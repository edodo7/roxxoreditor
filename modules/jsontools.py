#!/bin/python3
# -*- coding: utf-8 -*-

import json

# Global variables
global content

def read(filename):
	""" Reads the file specified by the filename and returns the content
	as a python dict.

	Keyword arguments:
	filename -- The name of the file with the contents to process.
	"""
	content = json.loads(filename)

	return content

def selectItem():
	"""
	"""
	# ToDo
