# -*- coding: utf-8 -*-
"""Module ga4gh.drs.util.functions.hashfunc.py
Contains functions for getting hashing function digests from large objects
for the various supported hashing functions
"""

import crc32c
import hashlib

def hashfunc_md5(input_file):
    """Get an md5 hash digest from a large input file

    Arguments:
        input_file (str): path to input file
    
    Returns:
        (str): md5 digest of file contents
    """
    
    hash_func = hashlib.md5()
    with open(input_file, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_func.update(chunk)
    return hash_func.hexdigest()
    

def hashfunc_crc32c(input_file):
    """Get a crc32c hash digest from a large input file

    Arguments:
        input_file (str): path to input file
    
    Returns:
        (str): crc32c digest of file contents
    """

    #TODO: get hashfunc crc32c to work correctly
    content = open(input_file, "rb").read()
    digest = crc32c.crc32(content)
    return digest
