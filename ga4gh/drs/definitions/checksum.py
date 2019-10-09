# -*- coding: utf-8 -*-
"""Module ga4gh.drs.definitions.checksum.py
Contains class representation of "6.3 Checksum" object outlined in DRS 
specification. Contains the checksum digest of an object, as well as the 
hashing algorithm used to generate the digest.
"""

from ga4gh.drs.util.functions.hashfunc import *

class Checksum(object):
    """Checksum digest of a DRS object

    Attributes:
       HASHFUNCS (dict): class attr, maps hashfunc name to matching function
       RANKED_HASHFUNCS (list): class attr, hierarchy of hash functions to use
       json (dict): parsed Checksum JSON, used to set other attributes
       checksum (str): checksum digest value of DRSObject object
       type (str): name of hashing function used to produce checksum
    """

    HASHFUNCS = {
        "md5": hashfunc_md5,
        "sha-256": hashfunc_sha256,
        "sha256": hashfunc_sha256,
        "SHA256": hashfunc_sha256,
        "crc32c": hashfunc_crc32c,
        "etag": hashfunc_md5
    }

    RANKED_HASHFUNCS = [
        "md5",
        "sha-256",
        "sha256",
        "SHA256",
        "crc32c",
        "etag"
    ]

    def __init__(self, json):
        """Instantiates a Checksum object

        Arguments:
            json (dict): parsed Checksum JSON
        """
        
        self.json = json
        self.checksum = self.__initialize_checksum()
        self.type = self.__initialize_type()

    def __initialize_checksum(self):
        """Initializes value of checksum property

        Returns:
            (str): checksum digest
        """

        return self.json["checksum"]
    
    def __initialize_type(self):
        """Initializes value of type property

        Returns:
            (str): checksum type
        """

        return self.json["type"]
