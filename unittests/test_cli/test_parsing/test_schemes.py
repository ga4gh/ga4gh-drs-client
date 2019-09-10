# -*- coding: utf-8 -*-
"""Module unittests.test_parsing.test_schemes.py
Unit tests for schemes cli parsing
"""

from click.testing import CliRunner
from ga4gh.drs.cli.parsing.schemes import schemes as schemes_group
from ga4gh.drs.cli.parsing.schemes import ls as schemes_ls
from unittests.cli_kwargs import ARGS_0

def test_schemes_group():

    runner = CliRunner()
    result = runner.invoke(schemes_group, ["--help"])
    assert result.exit_code == 0

def test_schemes_ls_parsing():

    runner = CliRunner()
    result = runner.invoke(schemes_ls, [])
    assert result.exit_code == 0
