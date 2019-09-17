# -*- coding: utf-8 -*-
"""Module ga4gh.drs.config.constants.py
Global settings and constants used by the drs client package

Attributes:
    HTTPS_BASE_PATH (str): base path to drs objects according to spec
    HttpStatusCode (class): int representations of http status codes
"""



HTTPS_BASE_PATH = "/ga4gh/drs/v1"

class HttpStatusCode(object):
    """Contains int representations of different http status codes"""

    OK = 200
    CREATED = 201
    ACCEPTED = 202
    PARTIAL_CONTENT = 206
