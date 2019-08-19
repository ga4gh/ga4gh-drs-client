import requests

class Route(object):

    def __init__(self, base_url, object_id):
        self.props = {}
        self.set_base_url(base_url)
        self.set_object_id(object_id)
        self.template = "/"
    
    def format_endpoint(self):
        return str.format(self.template, **self.props)

    def full_url(self):
        return self.get_base_url() + self.format_endpoint()

    def construct_request(self):
        url = self.full_url()
        headers = {}
        params = {}

        return [url, headers, params]

    def issue_request(self):
        url, headers, params = self.construct_request()
        return requests.get(self.full_url())
    
    def set_base_url(self, base_url):
        self.props["base_url"] = base_url
    
    def get_base_url(self):
        return self.props["base_url"]

    def set_object_id(self, object_id):
        self.props["object_id"] = object_id
    
    def get_object_id(self):
        return self.props["object_id"]
