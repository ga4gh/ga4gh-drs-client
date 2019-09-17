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
        self.access_id = self.__initialize_access_id()
        self.access_url = self.__initialize_access_url()
        self.region = self.__initialize_region()
        self.type = self.__initialize_type()

    def set_access_url(self, access_url):
        """Set the access_url property to a new AccessUrl

        Arguments:
            access_url (AccessUrl): new access url object
        """

        self.access_url = access_url
    
    def __initialize_access_id(self):
        """Initializes value of access_id property

        Returns:
            (str): access id
        
        """

        access_id = self.json["access_id"] \
                    if "access_id" in self.json.keys() \
                    else None
        return access_id
    
    def __initialize_access_url(self):
        """Initializes value of access_url property

        Returns:
            (AccessUrl): access url
        """

        access_url = AccessUrl(self.json["access_url"], self) \
                     if "access_url" in self.json.keys() \
                     else None
        return access_url
    
    def __initialize_region(self):
        """Initializes value of region property

        Returns:
            (str): region
        """

        region = self.json["region"] \
                 if "region" in self.json.keys() \
                 else None
        return region
    
    def __initialize_type(self):
        """Initializes value of type property

        Returns:
            (str): type
        """

        return self.json["type"]

