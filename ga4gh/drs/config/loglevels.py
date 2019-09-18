"""Module ga4gh.drs.config.loglevels.py
Logging-related attributes

Attributes:
    LOGLEVELS (dict): maps level keywords to corresponding int
"""

import logging

LOGLEVELS = {
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR
}