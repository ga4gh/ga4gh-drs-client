# -*- coding: utf-8 -*-
"""Module ga4gh.drs.cli.parsing.get.py
Click arguments expected by and passed to the 'get' command 
"""

import click
import os
from ga4gh.drs.cli.methods import get as drsget

@click.command()
@click.argument('url')
@click.argument('object_id')
@click.option("--authtoken", "-t", 
    help="Value of OAuth 2.0 Authorization: Bearer token")
@click.option("--download", "-d", is_flag=True, 
    help="Flag. If set, download object bytes")
@click.option("--expand", "-x", is_flag=True, 
    help="Flag. If set, program will recursively traverse inner bundles within "
         + "the root bundle")
@click.option("--logfile", "-l", help="File to which logs should be written")
@click.option("--max-threads", "-M", type=click.IntRange(1,), default=1,
    show_default=True, help="Number of concurrent download threads")
@click.option("--output-dir", "-o", default=os.getcwd(),
    help="Directory to write downloaded files")
@click.option("--output-metadata", "-m",
    help="File to write object metadata (printed to stdout by default)")
@click.option("--silent", "-S", is_flag=True,
    help="Flag. If set, don't output any messages to console or log file")
@click.option("--suppress-ssl-verify", "-s", is_flag=True,
    help="Flag. If set, suppress ssl certificate verification "
         + "(NOT RECOMMENDED)")
@click.option("--validate-checksum", "-v", is_flag=True, 
    help="Flag. If set, perform checksum validation on downloaded objects")
@click.option("--verbosity", "-V", 
    type=click.Choice(["DEBUG", "INFO", "WARNING", "ERROR"]),
    help="Control verbosity of logging")
def get(**kwargs):
    """get an object or bundle from a DRS service"""

    drsget.get(**kwargs)