# -*- coding: utf-8 -*-
"""Module ga4gh.drs.config.download_status.py
Download Status Constants

Attributes:
    DownloadStatus (class): int representations of different download states
    DOWNLOAD_STATUS (dict): maps download status int to string representation
"""

class DownloadStatus(object):
    """Contains int representations of different download states"""

    NOT_STARTED = 0
    STARTED = 1
    COMPLETED = 2
    FAILED = -1

DOWNLOAD_STATUS = {
    DownloadStatus.NOT_STARTED: "NOT STARTED",
    DownloadStatus.STARTED: "STARTED",
    DownloadStatus.COMPLETED: "COMPLETED",
    DownloadStatus.FAILED: "FAILED"
}