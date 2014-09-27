#!/bin/python3
# -*- coding: utf-8 -*-

import json

def read(filename):
    """ Reads the file specified by the filename and returns the content
        as a python dict.

    Keyword arguments:
        filename -- The name of the file with the contents to process.
    """
    return json.loads(filename)


def write(filename, content):
    """ Writes the given content into the specified filename.

    Keyword arguments:
        filename -- The name of the file in which the contents will be write.
        content  -- The content to write into the file.
    """
    str_dump = json.dumps(content, indent=4, separators=(',', ': '))

    with open(filename, 'w') as foutput:
        foutput.writelines(str_dump)
