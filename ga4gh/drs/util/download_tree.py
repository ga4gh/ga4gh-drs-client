from ga4gh.drs.definitions.object import ContentsObject
from ga4gh.drs.definitions.object import Object
from ga4gh.drs.util.data_accessor import DataAccessor

from pkg_resources import resource_string, resource_listdir, resource_filename

import ga4gh.drs.config.globals as gl
import yaml

class DownloadTree(object):

    def __init__(self, drs_object):
        
        self.drs_object = drs_object
        self.contents_leaves = []
    
    def recurse_find_leaves(self, drs_object):

        for contents_object in drs_object.contents:
            
            if contents_object.is_bundle: # ContentsObject refers to a bundle
                                          # send this content object through
                                          # recursion
                self.recurse_find_leaves(contents_object)
            else: # ContentsObject refers to a single Object, add it to leaves
                self.contents_leaves.append(contents_object)
    
    def get_data_accessors_for_leaves(self, cli_kwargs, headers=None):

        data_accessors = []

        for contents in self.contents_leaves:
            drs_object = contents.get_corresponding_object(headers)
            if drs_object:
                da = DataAccessor(drs_object, cli_kwargs, headers)
                data_accessors.append(da)
        return data_accessors
    
    """
    def assign_access_methods_to_contents(self, dload_list):

        data_accessors = []

        for contents in dload_list:

            obj = None
            object_or_content_object = "ContentObject"

            if "access_methods" in contents.keys():
                if contents["access_methods"]:
                    contents_is_object = True

            if contents_is_object:
                obj = contents
            else:
                #TODO convert a ContentsObject to an Object
                print("Contents")
                print(contents)
                print("***")
        
            data_accessor = DataAccessor()
            supported_schemes = None
            supported_schemes_filename = resource_filename(
                'ga4gh.drs.resources', 'supported_schemes.yml')
            with open(supported_schemes_filename, "r") as f:
                supported_schemes = yaml.load(f, Loader=yaml.FullLoader)["schemes"]

            for acc_method_json in obj["access_methods"]:
                acc_type = acc_method_json["type"]

                if supported_schemes[acc_type]:
                    acc_method_obj = gl.ACCESS_METHODS[acc_type](acc_method_json)
                    data_accessor.add_access_method(acc_method_obj)
            data_accessors.append(data_accessor)

        return data_accessors
    """