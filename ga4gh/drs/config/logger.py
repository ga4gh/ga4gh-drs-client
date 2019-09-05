"""Module ga4gh.drs.config.logger.py
Logging-related attributes

Attributes:
    logger (Logger): global logger that any module can use to log
    LOGLEVELS (dict): maps level keywords to corresponding int
"""

import logging
from ga4gh.drs.util.logger import Logger

logger = Logger("drs.logger")

LOGLEVELS = {
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR
}