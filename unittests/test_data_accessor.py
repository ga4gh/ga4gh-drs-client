# -*- coding: utf-8 -*-
"""Module unittests.test_data_accessor.py
Unit tests for data accessor module
"""

import ga4gh.drs.config.download_status as ds
import ga4gh.drs.config.checksum_status as cs
import json
import os
from ga4gh.drs.util.download_tree import DownloadTree
from ga4gh.drs.util.download_manager import DownloadManager
from ga4gh.drs.definitions.object import DRSObject
from unittests.cli_kwargs import CLI_KWARGS_0

drs_inner_bundle_json = open("unittests/testdata/json/drs_object_3.json", "r").read()
drs_inner_bundle_obj = json.loads(drs_inner_bundle_json)
drs_inner_bundle = DRSObject(drs_inner_bundle_obj, CLI_KWARGS_0)

def test_data_accessor():

    dt = DownloadTree(drs_inner_bundle)
    dt.recurse_find_leaves(drs_inner_bundle)
    data_accessors = dt.get_data_accessors_for_leaves(CLI_KWARGS_0)
    checksum_statuses = [
        cs.ChecksumStatus.FAILED,
        cs.ChecksumStatus.PASSED,
        cs.ChecksumStatus.PASSED,
        cs.ChecksumStatus.FAILED
    ]

    for i in range(0, len(data_accessors)):
        data_accessor = data_accessors[i]
        data_accessor.download()
        data_accessor.validate_checksum()
        assert data_accessor.checksum_status == checksum_statuses[i]
