# -*- coding: utf-8 -*-
"""Module ga4gh.drs.util.logger.py
Contains class definition of global logger
"""

import logging

class Logger(object):
    """Global logger

    Attributes:
        format (str): log message format
        formatter (Formatter): logging.Formatter object
        logger (Logger): logging.Logger object
    """

    def __init__(self, name):
        """Instantiates a Logger object

        Arguments:
            name (str): name of logger
        """

        self.format = "%(asctime)s\t%(levelname)s\t%(message)s"
        self.formatter = logging.Formatter(self.format)
        self.logger = logging.getLogger(name)

    def set_handler(self, logfile=None, loglevel=logging.DEBUG):
        """Set the logger's handler based on requested output location

        Arguments:
            logfile (str): path to logfile, or None if logging to stdout
            loglevel (int): log level of logger
        """

        self.logger.setLevel(loglevel) 

        # if a logfile is specified, create a logging file handler, setting
        # its loglevel and formatter, then adding it to the logger
        # otherwise, configure the logger so it will print to stdout
        if logfile:
            fh = logging.FileHandler(logfile)
            fh.setLevel(logging.DEBUG)
            fh.setFormatter(self.formatter)
            self.logger.addHandler(fh)
        else:
            logging.basicConfig(format=self.format)

    def debug(self, message):
        """Log a message at the DEBUG log level

        Arguments:
            message (str): message to log
        """
        
        self.logger.debug(message)

    def info(self, message):
        """Log a message at the INFO log level

        Arguments:
            message (str): message to log
        """

        self.logger.info(message)

    def warning(self, message):
        """Log a message at the WARNING log level

        Arguments:
            message (str): message to log
        """

        self.logger.warning(message)
    
    def error(self, message):
        """Log a message at the ERROR log level

        Arguments:
            message (str): message to log
        """

        self.logger.error(message)
