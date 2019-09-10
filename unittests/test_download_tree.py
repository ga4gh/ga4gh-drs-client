# -*- coding: utf-8 -*-
"""Module unittests.test_download_tree.py
Unit tests for download tree module
"""

import json
from ga4gh.drs.util.download_tree import DownloadTree
from ga4gh.drs.definitions.object import DRSObject
from unittests.cli_kwargs import CLI_KWARGS_0

drs_bundle_json = open("unittests/testdata/json/drs_object_2.json", "r").read()
drs_bundle_obj = json.loads(drs_bundle_json)
drs_bundle = DRSObject(drs_bundle_obj, CLI_KWARGS_0)

drs_inner_bundle_json = open("unittests/testdata/json/drs_object_3.json", "r").read()
drs_inner_bundle_obj = json.loads(drs_inner_bundle_json)
drs_inner_bundle = DRSObject(drs_inner_bundle_obj, CLI_KWARGS_0)

def test_download_tree():

    dt = DownloadTree(drs_bundle)
    assert len(dt.contents_leaves) == 0

    dt.recurse_find_leaves(drs_bundle)
    assert len(dt.contents_leaves) == 2

    data_accessors = dt.get_data_accessors_for_leaves(CLI_KWARGS_0)
    assert len(data_accessors) == 2

def test_download_tree_recursive_bundle():

    dt = DownloadTree(drs_inner_bundle)
    assert len(dt.contents_leaves) == 0

    dt.recurse_find_leaves(drs_inner_bundle)
    assert len(dt.contents_leaves) == 4

    data_accessors = dt.get_data_accessors_for_leaves(CLI_KWARGS_0)
    assert len(data_accessors) == 4
