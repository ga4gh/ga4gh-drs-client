# -*- coding: utf-8 -*-
"""Module unittests.test_util.test_functions.test_http.py
Unit tests for http functions module
"""

from ga4gh.drs.util.functions.http import header_list_to_dict

header_list = [
    "Authorization: abcdefghi123456789",
    "Accept: application/json"
]

def test_header_list_to_dict():

    header_dict = header_list_to_dict(header_list)
    assert header_dict["Authorization"] == "abcdefghi123456789"
    assert header_dict["Accept"] == "application/json"
