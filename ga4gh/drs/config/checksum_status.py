# -*- coding: utf-8 -*-
"""Module ga4gh.drs.config.checksum_status.py
Checksum Status Config Variables

Attributes:
    ChecksumStatus (class): int representations of checksum validation results
    CHECKSUM_STATUS (dict): maps checksum status int to string representation
"""

class ChecksumStatus(object):
    """Contains int representations of different checksum validation results"""

    NOT_APPLICABLE = 0
    PASSED = 1
    FAILED = -1

CHECKSUM_STATUS = {
    ChecksumStatus.NOT_APPLICABLE: "N/A",
    ChecksumStatus.PASSED: "PASSED",
    ChecksumStatus.FAILED: "FAILED"
}