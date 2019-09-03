# -*- coding: utf-8 -*-
"""Module ga4gh.drs.cli.parsing.schemes.py
Click arguments expected by and passed to the under the 'schemes' group of 
commands
"""

import click

@click.group()
def schemes():
    """view/update supported url schemes"""

    pass

@schemes.command()
def ls():
    """Executes the 'drs schemes ls' command after parsing cli args/opts"""

    pass

@schemes.command()
def update_supported():
    """Executes the 'drs schemes update-supported' command after parsing args"""
    
    pass

