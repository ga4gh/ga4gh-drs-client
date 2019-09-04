# -*- coding: utf-8 -*-
"""Module ga4gh.drs.util.functions.hashfunc.py
Contains the DownloadTree class, which recurses through the "contents" property
of a (bundle) DRSObject, to find all the non-bundle, single object DRSObjects.
Also recurses through bundles-within-bundles to get all the single objects
within a bundle tree.
"""

import yaml
from ga4gh.drs.definitions.object import ContentsObject
from ga4gh.drs.definitions.object import Object
from ga4gh.drs.util.data_accessor import DataAccessor
from pkg_resources import resource_string, resource_listdir, resource_filename

class DownloadTree(object):
    """Finds all single-object nodes in a bundle tree/hierarchy

    Attributes:
        drs_object (DRSObject): reference to the root DRSObject bundle
        contents_leaves (list): all single-object termini nodes in bundle
    """

    def __init__(self, drs_object):
        """Instantiates a DownloadTree object

        Arguments:
            drs_object (DRSObject): reference to the root DRSObject bundle
        """
        
        self.drs_object = drs_object
        self.contents_leaves = []
    
    def recurse_find_leaves(self, drs_object):
        """Find all non-bundle ContentsObjects from a root bundle

        Arguments:
            drs_object (DRSObject): reference to a bundle DRSObject
        """

        for contents_object in drs_object.contents:
            
            if contents_object.is_bundle: # ContentsObject refers to a bundle
                                          # send this content object through
                                          # recursion
                self.recurse_find_leaves(contents_object)
            else: # ContentsObject refers to a single Object, add it to leaves
                self.contents_leaves.append(contents_object)
    
    def get_data_accessors_for_leaves(self, cli_kwargs, headers=None):
        """Convert all ContentsObjects to DRSObjects

        Arguments:
            cli_kwargs (dict): command-line arguments dict
            headers (dict): headers for DRS requests

        Returns:
            (list): list of DataAccessors, one per element in contents_leaves
        """

        data_accessors = []
        for contents in self.contents_leaves:
            drs_object = contents.get_corresponding_object()
            if drs_object:
                da = DataAccessor(drs_object, cli_kwargs, headers)
                data_accessors.append(da)
        return data_accessors
