import ga4gh.drs.config.globals as gl
from ga4gh.drs.definitions.access_url import AccessUrl

class AccessMethod(object):

    def __init__(self, json, drs_obj):
        self.json = json
        self.drs_obj = drs_obj
        self.access_id = None
        self.access_url = None
        self.region = None
        self.type = None

        self.__set_access_id()
        self.__set_access_url()
        self.__set_region()
        self.__set_type()
    
    def __set_access_id(self):
        if "access_id" in self.json.keys():
            self.access_id = self.json["access_id"]
    
    def __set_access_url(self):
        if "access_url" in self.json.keys():
            self.access_url = AccessUrl(self.json["access_url"])
    
    def __set_region(self):
        if "region" in self.json.keys():
            self.region = self.json["region"]
    
    def __set_type(self):
        self.type = self.json["type"]