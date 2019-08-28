# -*- coding: utf-8 -*-
"""Module ga4gh.drs.exceptions.drs_exceptions.py
Contains Exception subclasses for unique exceptions encountered when running
the DRS client application
"""

class DRSException(Exception):
    """General exception thrown for DRS client-related exceptions"""

    def __init__(self, message):
        """Instantiates a DRSException object

        Arguments:
            message (str): message explaining the encountered exception
        """

        super(DRSException, self).__init__(message)
        self.message = message
    
    def __str__(self):
        """Get string representation of the DRSException

        Returns:
            (str): string representation of DRSException
        """

        return self.__class__.__name__ + "\t" + self.message

class CLIException(DRSException):
    """For issues pertaining to supplied command-line arguments/options"""

    pass

class StatusCodeException(DRSException):
    """For issues pertaining to unexpected response status codes"""

    pass

class SSLException(DRSException):
    """For issues pertaining to unexpected behaviour during SSL validation"""

    pass

class DownloadSubmethodException(DRSException):
    """For issues pertaining to problems encountered during download attempts"""

    pass
        