#!/bin/python3
# -*- coding: utf-8 -*-

def extractDataStructure(dataStruct, path: list):
    """ Extract the sub data structure defined by the path from dataStruct.

    Keyword arguments:
        dataStruct -- The data structure in wich we search for the sub data
                          structure.
        path       -- The path to the sub data structure.
    """
    for i in range(len(path)):
        dataStruct = dataStruct[path[i]]
    return dataStruct
