import logging
from ga4gh.drs.util.logger import Logger
from ga4gh.drs.util.method_types.gs import GS

logger = Logger("drs.logger")

HTTPS_BASE_PATH = "/ga4gh/drs/v1"

LOGLEVELS = {
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR
}

ACCESS_METHOD_TYPES = {
    "gs": GS
}

class DownloadStatus(object):

    NOT_STARTED = 0
    STARTED = 1
    COMPLETED = 2
    FAILED = -1

class ChecksumStatus(object):

    NOT_APPLICABLE = 0
    PASSED = 1
    FAILED = -1

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