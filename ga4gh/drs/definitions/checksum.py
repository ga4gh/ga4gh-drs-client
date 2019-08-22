class Checksum(object):

    def __init__(self, json):
        
        self.json = json
        self.checksum = self.__initialize_checksum()
        self.type = self.__initialize_type()

    def __initialize_checksum(self):
        return self.json["checksum"]
    
    def __initialize_type(self):
        return self.json["type"]