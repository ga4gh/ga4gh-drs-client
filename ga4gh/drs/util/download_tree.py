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
            drs_object = contents.get_corresponding_object(cli_kwargs)
            if drs_object:
                da = DataAccessor(drs_object, cli_kwargs, headers)
                data_accessors.append(da)
        return data_accessors
