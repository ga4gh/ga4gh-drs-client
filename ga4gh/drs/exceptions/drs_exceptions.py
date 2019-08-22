class DRSException(Exception):

    def __init__(self, message):
        super(DRSException, self).__init__(message)
        self.message = message
    
    def __str__(self):
        return self.__class__.__name__ + "\t" + self.message

class CLIException(DRSException):
    pass

class StatusCodeException(DRSException):
    pass

class SSLException(DRSException):
    pass

class DownloadSubmethodException(DRSException):
    pass
        