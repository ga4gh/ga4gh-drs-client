import re
import requests
import json

from ga4gh.drs.config.globals import ACCESS_METHOD_TYPES
from ga4gh.drs.definitions.checksum import Checksum

class Object(object):
    
    def __initialize_contents(self):
        
        contents = []
        if "contents" in self.json.keys():
            if self.json["contents"]:
                for contents_json in self.json["contents"]:
                    new_contents = ContentsObject(contents_json)
                    contents.append(new_contents)
        
        return contents
    
    def __initialize_is_bundle(self):
        return True if len(self.contents) > 0 else False

class DRSObject(Object):

    def __init__(self, json):

        self.json = json
        self.access_methods = self.__initialize_access_methods()
        self.aliases = self.__initialize_aliases()
        self.checksums = self.__initialize_checksums()
        self.contents = self._Object__initialize_contents()
        self.created_time = self.__initialize_created_time()
        self.description = self.__initialize_description()
        self.id = self.__initialize_id()
        self.mime_type = self.__initialize_mime_type()
        self.name = self.__initialize_name()
        self.self_uri = self.__initialize_self_uri()
        self.size = self.__initialize_size()
        self.updated_time = self.__initialize_updated_time()
        self.version = self.__initialize_version()
        self.is_bundle = self._Object__initialize_is_bundle()
    
    def __initialize_access_methods(self):
        
        access_methods = []
        if "access_methods" in self.json.keys():
            if self.json["access_methods"]:
                for access_json in self.json["access_methods"]:
                    access_class = ACCESS_METHOD_TYPES[access_json["type"]]
                    access_obj = access_class(access_json, self)
                    access_methods.append(access_obj)

        return access_methods
    
    def __initialize_aliases(self):
        return self.json["aliases"] if "aliases" in self.json.keys() else None
    
    def __initialize_checksums(self):
        checksums = []
        for checksum_json in self.json["checksums"]:
            checksum_obj = Checksum(checksum_json)
            checksums.append(checksum_obj)
        return checksums
    
    def __initialize_created_time(self):
        return self.json["created_time"]
    
    def __initialize_description(self):
        return self.json["description"] \
               if "description" in self.json.keys() \
               else None
    
    def __initialize_id(self):
        return self.json["id"]
    
    def __initialize_mime_type(self):
        return self.json["mime_type"] \
               if "mime_type" in self.json.keys() \
               else None
    
    def __initialize_name(self):
        return self.json["name"] if "name" in self.json.keys() else None
    
    def __initialize_self_uri(self):
        return self.json["self_uri"]
    
    def __initialize_size(self):
        return self.json["size"]
    
    def __initialize_updated_time(self):
        return self.json["updated_time"] \
               if "updated_time" in self.json.keys() \
               else None
    
    def __initialize_version(self):
        return self.json["version"] if "version" in self.json.keys() else None

class ContentsObject(Object):

    def __init__(self, json):
        self.json = json
        self.contents = self._Object__initialize_contents()
        self.drs_uri = self.__initialize_drs_uri()
        self.id = self.__initialize_id()
        self.name = self.__initialize_name
        self.is_bundle = self._Object__initialize_is_bundle()
    
    def get_corresponding_object(self, headers=None):
        matching_obj = None
        
        for drs_uri in self.drs_uri:
            
            try:
                if matching_obj == None:
                    #TODO: remove drs url modifications
                    subbed_uri = re.sub("^drs", "https", drs_uri)
                    s = subbed_uri.split("/")
                    new_uri = "/".join(s[:-1])+"/ga4gh/drs/v1/objects/"+s[-1]
                    
                    response = requests.get(new_uri, headers=headers)
                    # response = requests.get(new_uri)
                    obj_json = json.loads(response.content)
                    drs_obj = DRSObject(obj_json)
                    matching_obj = drs_obj
            except Exception as e:
                pass
        
        return matching_obj
    
    def __initialize_drs_uri(self):
        return self.json["drs_uri"] if "drs_uri" in self.json.keys() else None
    
    def __initialize_id(self):
        return self.json["id"] if "id" in self.json.keys() else None
    
    def __initialize_name(self):
        return self.json["name"]