import logging

class Logger(object):

    def __init__(self, name):
        self.format = "%(asctime)s\t%(levelname)s\t%(message)s"
        self.formatter = logging.Formatter(self.format)
        self.logger = logging.getLogger(name)

    def set_handler(self, logfile=None, loglevel=logging.DEBUG):
        self.logger.setLevel(loglevel) 

        if logfile:
            fh = logging.FileHandler(logfile)
            fh.setLevel(logging.DEBUG)
            fh.setFormatter(self.formatter)
            self.logger.addHandler(fh)
        else:
            logging.basicConfig(format=self.format)

    def debug(self, message):
        self.logger.debug(message)

    def info(self, message):
        self.logger.info(message)

    def warning(self, message):
        self.logger.warning(message)
    
    def error(self, message):
        self.logger.error(message)