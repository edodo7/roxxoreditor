#!/usr/bin/python3
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

def cleanDataStructure(dataStruct):
    """ Walk around the entire data structure dataStruct and copy it but set
        all the data to a default value.
        Default values:
        int   -> 0
        float -> 0.0
        None  -> None
        str   -> ""

    Keyword arguments:
        dataStruct -- The data structure to clean.
    """
    def cleanData(data):
        """ Return a default value according to the type of data.

        Keyword arguments:
        data -- The data to get the default value.
        """
        if data == None:
            return None
        elif type(data) == int:
            return 0
        elif type(data) == float:
            return 0.0
        elif type(data) == str:
            return ""

    if type(dataStruct) == list:
        new = list()
        for i in range(len(dataStruct)):
            if type(dataStruct[i]) == list or type(dataStruct[i]) == dict:
                new.append(cleanDataStructure(dataStruct[i]))
            else:
                new.append(cleanData(dataStruct[i]))
        return new
    else:
        new = dict()
        keyList = dataStruct.keys()
        for key in keyList:
            if type(dataStruct[key]) == list or type(dataStruct[key]) == dict:
                new[key] = cleanDataStructure(dataStruct[key])
            else:
                new[key] = cleanData(dataStruct[key])
        return new
