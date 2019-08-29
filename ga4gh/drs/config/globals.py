# -*- coding: utf-8 -*-
"""Module ga4gh.drs.config.globals.py
Global settings and constants used by the drs client package

Attributes:
    logger (Logger): global logger that any module can use to log
    HTTPS_BASE_PATH (str): base path to drs objects according to spec
    LOGLEVELS (dict): maps level keywords to corresponding int
    ACCESS_METHOD_TYPES (dict): maps scheme to the class that handles it
    DownloadStatus (class): int representations of different download states
    ChecksumStatus (class): int representations of checksum validation results
    HttpStatusCode (class): int representations of http status codes
    DOWNLOAD_STATUS (dict): maps download status int to string representation
    CHECKSUM_STATUS (dict): maps checksum status int to string representation
"""

import logging
from ga4gh.drs.util.logger import Logger
from ga4gh.drs.util.method_types.gs import GS
from ga4gh.drs.util.method_types.https import HTTPS

logger = Logger("drs.logger")

HTTPS_BASE_PATH = "/ga4gh/drs/v1"

LOGLEVELS = {
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR
}

ACCESS_METHOD_TYPES = {
    "gs": GS,
    "https": HTTPS
}

class DownloadStatus(object):
    """Contains int representations of different download states"""

    NOT_STARTED = 0
    STARTED = 1
    COMPLETED = 2
    FAILED = -1

class ChecksumStatus(object):
    """Contains int representations of different checksum validation results"""

    NOT_APPLICABLE = 0
    PASSED = 1
    FAILED = -1

class HttpStatusCode(object):
    """Contains int representations of different http status codes"""

    OK = 200
    CREATED = 201
    ACCEPTED = 202
    PARTIAL_CONTENT = 206

DOWNLOAD_STATUS = {
    DownloadStatus.NOT_STARTED: "NOT STARTED",
    DownloadStatus.STARTED: "STARTED",
    DownloadStatus.COMPLETED: "COMPLETED",
    DownloadStatus.FAILED: "FAILED"
}

CHECKSUM_STATUS = {
    ChecksumStatus.NOT_APPLICABLE: "N/A",
    ChecksumStatus.PASSED: "PASSED",
    ChecksumStatus.FAILED: "FAILED"
}
