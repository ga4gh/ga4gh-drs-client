# -*- coding: utf-8 -*-
"""Module ga4gh.drs.util.functions.hashfunc.py
Contains functions for getting hashing function digests from large objects
for the various supported hashing functions
"""

import crc32c
import hashlib
from base64 import b64decode, b64encode

def pad_hexdigest(s, n):
    """Pad a hex string with leading zeroes

    Arguments:
        s (str): input hex string
        n (int): number of expected characters in hex string
    
    Returns:
        (str): hex string padded with leading zeroes, such that its length is n 
    """

    return "0" * (n - len(s)) + s

def hashfunc_from_hashlib(hash_method, input_file):
    """Get a hash digest value from a large input file

    Arguments:
        hash_method (function): specific hashlib hashing algorithm
        input_file (str): path to input file
    
    Returns:
        (str): hash algorithm digest of file contents as a hex string
    """

    hashfunc = hash_method()
    with open(input_file, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hashfunc.update(chunk)
    return hashfunc.hexdigest()

def hashfunc_md5(input_file):
    """Get an md5 hash digest from a large input file

    Arguments:
        input_file (str): path to input file
    
    Returns:
        (str): md5 digest of file contents as a hex string
    """

    return hashfunc_from_hashlib(hashlib.md5, input_file)

def hashfunc_sha256(input_file):
    """Get an sha256 hash digest from a large input file

    Arguments:
        input_file (str): path to input file
    
    Returns:
        (str): sha256 digest of file contents as hex string
    """

    return hashfunc_from_hashlib(hashlib.sha256, input_file)

def hashfunc_crc32c(input_file):
    """Get a crc32c hash digest from a large input file

    Arguments:
        input_file (str): path to input file
    
    Returns:
        (str): crc32c digest of file contents as hex string
    """

    content = open(input_file, "rb").read()
    digest = crc32c.crc32(content)
    hex_string = hex(digest).split("x")[-1]
    hex_string_length = 8
    return pad_hexdigest(hex_string, hex_string_length)
