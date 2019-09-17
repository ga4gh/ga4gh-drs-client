# -*- coding: utf-8 -*-
"""Module ga4gh.drs.config.access_methods.py
Access Method-related Config Variables

Attributes:
    ACCESS_METHOD_TYPES (dict): maps scheme to the class that handles it
    ACCESS_METHOD_TYPES_DESC (dict): maps scheme to description message
"""

from ga4gh.drs.util.method_types.gs import GS
from ga4gh.drs.util.method_types.http import HTTP
from ga4gh.drs.util.method_types.https import HTTPS

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