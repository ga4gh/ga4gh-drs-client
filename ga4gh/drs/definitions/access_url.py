import requests

class AccessUrl(object):
    
    def __init__(self, json):
        self.json = json
        self.headers = self.__initialize_headers()
        self.url = self.__initialize_url()

    def issue_request(self):
        requests.get(self.url, headers=self.headers)

    def __initialize_headers(self):
        return self.json["headers"] if "headers" in self.json.keys() else {}
    
    def __initialize_url(self):
        return self.json["url"]

    def set_url(self, url):
        self.url = url
    
    def set_headers(self, headers):
        self.headers = headers

    def get_url(self):
        return self.url
    
    def get_headers(self):
        return self.headers