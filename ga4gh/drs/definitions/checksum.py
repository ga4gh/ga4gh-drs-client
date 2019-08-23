from ga4gh.drs.util.functions.hashfunc import *

class Checksum(object):

    HASHFUNCS = {
        "md5": hashfunc_md5,
        "crc32c": hashfunc_crc32c
    }

    RANKED_HASHFUNCS = [
        "crc32c",
        "md5"
    ]

    def __init__(self, json):
        
        self.json = json
        self.checksum = self.__initialize_checksum()
        self.type = self.__initialize_type()

    def __initialize_checksum(self):
        return self.json["checksum"]
    
    def __initialize_type(self):
        return self.json["type"]