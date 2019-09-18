# -*- coding: utf-8 -*-
"""Module unittests.test_download_manager.py
Unit tests for download manager module
"""

import ga4gh.drs.config.download_status as ds
import json
import os
from ga4gh.drs.util.download_tree import DownloadTree
from ga4gh.drs.util.download_manager import DownloadManager
from ga4gh.drs.definitions.object import DRSObject
from unittests.cli_kwargs import CLI_KWARGS_0

drs_inner_bundle_json = open("unittests/testdata/json/drs_object_3.json", "r").read()
drs_inner_bundle_obj = json.loads(drs_inner_bundle_json)
drs_inner_bundle = DRSObject(drs_inner_bundle_obj)

exp_download_statuses = [
    ds.DownloadStatus.COMPLETED,
    ds.DownloadStatus.COMPLETED,
    ds.DownloadStatus.COMPLETED,
    ds.DownloadStatus.COMPLETED
]

def test_download_manager():

    dt = DownloadTree(drs_inner_bundle)
    dt.recurse_find_leaves(drs_inner_bundle)
    data_accessors = dt.get_data_accessors_for_leaves()
    assert len(data_accessors) == 4

    dm = DownloadManager(data_accessors)
    assert len(dm.data_accessors) == 4
    assert dm.max_workers == 1
    assert dm.report_file == "unittests/outdata/drs_download_report.txt"

    for da in dm.data_accessors:
        assert da.download_status == ds.DownloadStatus.NOT_STARTED

    dm.execute_thread_pool()

    for i in range(0, len(data_accessors)):
        da = data_accessors[i]
        assert da.download_status == exp_download_statuses[i]

    dm.write_report()
    assert os.path.exists("unittests/outdata/drs_download_report.txt")
    
test_download_manager()