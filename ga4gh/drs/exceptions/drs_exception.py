class DRSException(Exception):

    def __init__(self, message):
        super(DRSException, self).__init__(message)
        self.message = message
    
    def __str__(self):
        return "Error: " + self.message
        