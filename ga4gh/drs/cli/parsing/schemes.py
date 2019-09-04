# -*- coding: utf-8 -*-
"""Module ga4gh.drs.cli.parsing.schemes.py
Click arguments expected by and passed to the under the 'schemes' group of 
commands
"""

import click
from ga4gh.drs.cli.methods import schemes as drsschemes

@click.group()
def schemes():
    """view supported url schemes"""

    pass

@schemes.command()
def ls(**kwargs):
    """list supported schemes"""

    drsschemes.ls(**kwargs)

# @schemes.command()
# def update_supported():
#     """Executes the 'drs schemes update-supported' command after parsing args"""
#     
#     pass

