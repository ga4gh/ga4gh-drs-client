# -*- coding: utf-8 -*-
"""Module unittests.test_util.test_functions.test_hashfunc.py
Unit tests for http functions module
"""

from ga4gh.drs.util.functions.hashfunc import hashfunc_crc32c

def test_crc32c():
    
    input_file = "unittests/testdata/bam/unittest.bam"
    digest = hashfunc_crc32c(input_file)
    assert digest == 4030027759
