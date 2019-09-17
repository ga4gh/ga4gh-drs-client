# -*- coding: utf-8 -*-
"""Module ga4gh.drs.config.constants.py
Global settings and constants used by the drs client package

Attributes:
    HTTPS_BASE_PATH (str): base path to drs objects according to spec
    ACCESS_METHOD_TYPES (dict): maps scheme to the class that handles it
    ChecksumStatus (class): int representations of checksum validation results
    HttpStatusCode (class): int representations of http status codes
    CHECKSUM_STATUS (dict): maps checksum status int to string representation
"""

from ga4gh.drs.util.method_types.gs import GS
from ga4gh.drs.util.method_types.http import HTTP
from ga4gh.drs.util.method_types.https import HTTPS

HTTPS_BASE_PATH = "/ga4gh/drs/v1"

ACCESS_METHOD_TYPES = {
    "gs": GS,
    "http": HTTP,
    "https": HTTPS,
}

ACCESS_METHOD_TYPES_DESC = {
    "gs": "Google Cloud Storage",
    "http": "Hypertext Transfer Protocol",
    "https": "Hypertext Transfer Protocol Secure"
}

class HttpStatusCode(object):
    """Contains int representations of different http status codes"""

    OK = 200
    CREATED = 201
    ACCEPTED = 202
    PARTIAL_CONTENT = 206
