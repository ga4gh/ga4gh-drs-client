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