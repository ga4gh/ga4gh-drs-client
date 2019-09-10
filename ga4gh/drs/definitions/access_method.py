# -*- coding: utf-8 -*-
"""Module ga4gh.drs.definitions.access_method.py
Contains class representation of "6.1 AccessMethod" object outlined in DRS 
specification. Indicates by what scheme, id, and/or url a DRS object can be
downloaded.
"""

from ga4gh.drs.definitions.access_url import AccessUrl

class AccessMethod(object):
    """Indicates by what scheme, id, and/or url a DRS object can be downloaded

    Attributes:
        json (dict): parsed AccessMethod JSON, used to set other attributes
        drs_obj (DRSObject): reference to parent DRSObject object
        access_id (str): arbitrary string, passed to the /access method
        access_url (AccessURL): url to fetch actual object bytes
        region (str): region in the cloud provider that object belongs to
        type (str): type/scheme of access method (eg. https, gs, ftp, etc.)
    """

    def __init__(self, json, drs_obj):
        """Instantiates an AccessMethod object

        Arguments:
            json (dict): parsed AccessMethod JSON
            drs_obj (DRSObject): reference to parent DRSObject object
        """

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
        """Initializes value of access_id property"""

        if "access_id" in self.json.keys():
            self.access_id = self.json["access_id"]
    
    def __set_access_url(self):
        """Initializes value of access_url property"""

        if "access_url" in self.json.keys():
            self.access_url = AccessUrl(self.json["access_url"], self)
    
    def __set_region(self):
        """Initializes value of region property"""

        if "region" in self.json.keys():
            self.region = self.json["region"]
    
    def __set_type(self):
        """Initializes value of type property"""

        self.type = self.json["type"]
