# -*- coding: utf-8 -*-
"""Module unittests.test_parsing.test_get.py
Unit tests for get cli parsing
"""

from click.testing import CliRunner
from ga4gh.drs.cli.parsing.get import get
from unittests.cli_kwargs import *

data = [
    {"args": ARGS_0, "exit_code": 0},
    {"args": ARGS_1, "exit_code": 0},
    {"args": ARGS_2, "exit_code": 0},
    {"args": ARGS_3, "exit_code": 2},
    {"args": ARGS_4, "exit_code": 0},
    {"args": ARGS_5, "exit_code": 0},
    {"args": ARGS_FAIL_0, "exit_code": 1},
    {"args": ARGS_FAIL_1, "exit_code": 1},
    {"args": ARGS_FAIL_2, "exit_code": 1},

]

def test_get_parsing():

    for test_i in data:
        runner = CliRunner()
        result = runner.invoke(get, test_i["args"])
        assert result.exit_code == test_i["exit_code"]

test_get_parsing()
