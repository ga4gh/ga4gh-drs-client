# -*- coding: utf-8 -*-
"""Module ga4gh.drs.definitions.object.py
Contains class representations of "6.4 ContentsObject" and "6.6 Object" objects 
outlined in DRS specification. Object represents a DRS object returned by a
request for a specific OBJECT_ID. ContentObject is a pared down representation
of an Object, primarily providing the url to access a full Object
"""

import json
import re
import requests
from ga4gh.drs.config.global_state import GLOBALSTATE
from ga4gh.drs.config.access_methods import ACCESS_METHOD_TYPES
from ga4gh.drs.definitions.checksum import Checksum
from ga4gh.drs.routes.route_fetch_bytes import RouteFetchBytes
from ga4gh.drs.routes.route_object_info import RouteObjectInfo
from ga4gh.drs.util.functions.url import *

class Object(object):
    """Parent class of DRSObject and ContentsObject.

    Attributes:
        json (dict): parsed Object JSON, used to set other attributes
        cli_kwargs (dict): command-line arguments/options
    """

    def __init__(self, json):
        """Instantiates an Object object

        Arguments:
            json (dict): parsed Object JSON, used to set other attributes
        """

        self.json = json
        self.cli_kwargs = GLOBALSTATE.get_prop("cli")
    
    def __initialize_contents(self):
        """Initializes value of "contents" property

        Returns:
            (list): array of ContentsObjects, one for each entry in "contents"
        """
        
        # The value of the 'contents' property is either null (for singular 
        # objects), or an array of ContentObject JSON (for bundles). If 
        # an array, create a ContentObject for each element in the array
        contents = []
        if "contents" in self.json.keys():
            if self.json["contents"]:
                for contents_json in self.json["contents"]:
                    new_contents = ContentsObject(
                        contents_json)
                    contents.append(new_contents)
        
        return contents
    
    def __initialize_is_bundle(self):
        """Initializes value of "is_bundle" property

        Returns:
            (bool): True if object is a bundle, False if singular object
        """

        # if the object's 'contents' property is an empty list, then this is a
        # singular object, but if 'contents' is populated, then this is a bundle
        return True if len(self.contents) > 0 else False

class DRSObject(Object):
    """DRS object returned by a request for a specific OBJECT_ID

    Attributes:
        access_methods (list): list of AccessMethods used to access bytes
        aliases (list): string aliases for this object
        checksums (list): list of Checksums, digest values for object bytes
        contents (list): list of child ContentObjects for bundle
        created_time (str): time object was created
        description (str): human readable description
        id (str): unique identifier of this object
        mime_type (str): optional mime-type of the object
        name (str): optional object name
        self_uri (str): drs URI used to access this object
        size (int): object blob size in bytes
        updated_time (str): optional date string object was last updated
        version (str): object version
        is_bundle (bool): True if object is bundle, False if singular object
    """

    def __init__(self, json):
        """Instantiates a DRSObject object

        Arguments:
            json (dict): parsed DRSObject JSON, used to set other attributes
        """

        super(DRSObject, self).__init__(json)
        self.id = self.__initialize_id()
        self.access_methods = self.__initialize_access_methods()
        self.aliases = self.__initialize_aliases()
        self.checksums = self.__initialize_checksums()
        self.contents = self._Object__initialize_contents()
        self.created_time = self.__initialize_created_time()
        self.description = self.__initialize_description()
        self.mime_type = self.__initialize_mime_type()
        self.name = self.__initialize_name()
        self.self_uri = self.__initialize_self_uri()
        self.size = self.__initialize_size()
        self.updated_time = self.__initialize_updated_time()
        self.version = self.__initialize_version()
        self.is_bundle = self._Object__initialize_is_bundle()
    
    def __initialize_access_methods(self):
        """Initializes value of access_methods property

        Returns:
            (list): list of AccessMethod subclasses according to type 
        """
        
        # for each JSON element in the 'access_methods' array, create an
        # AccessMethod subclass. The exact subclass instantiated is based on
        # the url scheme of the access_url's "url" property
        # if the object has an access_id instead of access_url, then first
        # convert the access_id to access_url via the access/<access_id> route
        access_methods = []
        if "access_methods" in self.json.keys():
            if self.json["access_methods"]:
                for access_json in self.json["access_methods"]:

                    valid_access_url_json = True

                    # issue request for the access_url if access_id provided
                    if access_json["access_id"]:
                        kwargs = self.cli_kwargs
                        route_fetch_bytes = RouteFetchBytes(
                            kwargs["url"],
                            self.id,
                            access_json["access_id"],
                            suppress_ssl_verify=kwargs["suppress_ssl_verify"],
                            authtoken=kwargs["authtoken"]
                        )
                        response = route_fetch_bytes.issue_request()
                        # attempt to parse access url json from the response
                        # to the access_id route
                        try:
                            response.raise_for_status()
                            access_url_json = response.json()
                            access_json["access_url"] = access_url_json
                        except Exception as e:
                            valid_access_url_json = False
                        
                    scheme = urlparse(access_json["access_url"]["url"]).scheme
                    if scheme in ACCESS_METHOD_TYPES.keys() \
                    and valid_access_url_json:
                        access_class = ACCESS_METHOD_TYPES[scheme]
                        access_obj = access_class(
                            access_json, self)
                        access_methods.append(access_obj)

        return access_methods
    
    def __initialize_aliases(self):
        """Initializes value of aliases property

        Returns:
            (list): aliases
        """

        return self.json["aliases"] if "aliases" in self.json.keys() else None
    
    def __initialize_checksums(self):
        """Initializes value of checksums property

        Returns:
            (list): Checksum objects
        """

        # creates a Checksum object for each element in the JSON array under
        # "checksums"
        checksums = []
        if "checksums" in self.json.keys():
            for checksum_json in self.json["checksums"]:
                checksum_obj = Checksum(checksum_json)
                checksums.append(checksum_obj)

        return checksums
    
    def __initialize_created_time(self):
        """Initializes value of created_time property

        Returns:
            (str): created time
        """

        return self.json["created_time"]
    
    def __initialize_description(self):
        """Initializes value of description property

        Returns:
            (str): description
        """

        return self.json["description"] \
               if "description" in self.json.keys() \
               else None
    
    def __initialize_id(self):
        """Initializes value of id property

        Returns:
            (str): id
        """

        return self.json["id"]
    
    def __initialize_mime_type(self):
        """Initializes value of mime_type property

        Returns:
            (str): mime-type
        """

        return self.json["mime_type"] \
               if "mime_type" in self.json.keys() \
               else None
    
    def __initialize_name(self):
        """Initializes value of name property

        Returns:
            (str): name
        """

        return self.json["name"] if "name" in self.json.keys() else None
    
    def __initialize_self_uri(self):
        """Initializes value of self_uri property

        Returns:
            (str): self_uri
        """

        return self.json["self_uri"]
    
    def __initialize_size(self):
        """Initializes value of size property

        Returns:
            (int): object size
        """

        return self.json["size"]
    
    def __initialize_updated_time(self):
        """Initializes value of updated_time property

        Returns:
            (str): updated time
        """

        return self.json["updated_time"] \
               if "updated_time" in self.json.keys() \
               else None
    
    def __initialize_version(self):
        """Initializes value of version property

        Returns:
            (str): version
        """

        return self.json["version"] if "version" in self.json.keys() else None

class ContentsObject(Object):
    """Pared down object stored under "contents" property of DRSObject

    Attributes:
        contents (list): list of child ContentObjects for bundle
        drs_uri (list): DRS urls/identifiers to retrieve this DRS Object
        id (str): unique identifier of this ContentsObject/DRSObject
        name (str): name of the ContentsObject
        is_bundle (bool): True if object is bundle, False if singular object
    """

    def __init__(self, json):
        """Instantiates a ContentsObject objects

        Arguments:
            json (dict): parsed ContentsObject JSON, used to set attributes
        """

        super(ContentsObject, self).__init__(json)
        self.contents = self._Object__initialize_contents()
        self.drs_uri = self.__initialize_drs_uri()
        self.id = self.__initialize_id()
        self.name = self.__initialize_name()
        self.is_bundle = self._Object__initialize_is_bundle()
    
    def get_corresponding_object(self):
        """Get the full matching DRSObject for this ContentsObject

        Arguments:
            kwargs (dict): cli arguments/options
        
        Returns:
            (DRSObject): full DRSObject matching ContentsObject
        """

        matching_obj = None
        kwargs = self.cli_kwargs

        for drs_uri in self.drs_uri:
            try:
                # if matching object hasn't been found, iterate through all 
                # uris in drs_uri list. Try to get DRSObject JSON from the 
                # "object info" route, using the base url and object_id
                # of the drs uri
                if matching_obj == None:
                    base_url, object_id = parse_drs_url(drs_uri)
                    route_obj_info = RouteObjectInfo(base_url, 
                        object_id,
                        kwargs["expand"], 
                        suppress_ssl_verify=kwargs["suppress_ssl_verify"],
                        authtoken=kwargs["authtoken"]
                    )
                    
                    response = route_obj_info.issue_request()
                    obj_json = json.loads(response.content)
                    drs_obj = DRSObject(obj_json)
                    matching_obj = drs_obj
            except Exception as e:
                pass
        
        return matching_obj
    
    def __initialize_drs_uri(self):
        """Initializes value of drs_uri property

        Returns:
            (list): drs uri(s)
        """

        return self.json["drs_uri"] if "drs_uri" in self.json.keys() else None
    
    def __initialize_id(self):
        """Initializes value of id property

        Returns:
            (str): id
        """

        return self.json["id"] if "id" in self.json.keys() else None
    
    def __initialize_name(self):
        """Initializes value of name property

        Returns:
            (str): name
        """

        return self.json["name"]
