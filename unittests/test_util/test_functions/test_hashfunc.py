# -*- coding: utf-8 -*-
"""Module unittests.test_util.test_functions.test_hashfunc.py
Unit tests for http functions module
"""

from ga4gh.drs.util.functions.hashfunc import *

def test_crc32c():
    
    input_file = "unittests/testdata/bam/unittest.bam"
    digest = hashfunc_crc32c(input_file)
    assert digest == "f03557ef"

def test_sha256():

    input_file = "unittests/testdata/bam/unittest.bam"
    digest = hashfunc_sha256(input_file)
    assert digest == "6809eab398594fb80a46623434d28f764a315de3946a6f578c16bbb2f5eb37b3"
