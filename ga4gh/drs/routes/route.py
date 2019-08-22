import requests
from ga4gh.drs.exceptions import drs_exceptions
from ga4gh.drs.util.functions.logging import *
import ga4gh.drs.config.globals as gl

class Route(object):

    def __init__(self, base_url, object_id, suppress_ssl_verify=False, 
        authtoken=None):

        self.logger = gl.logger
        self.props = {}
        self.set_base_url(base_url)
        self.set_object_id(object_id)
        self.ssl_verify = not suppress_ssl_verify
        self.authtoken = authtoken
        self.drs_base_path = "/ga4gh/drs/v1"
        self.template = "/"
    
    def format_endpoint(self):
        return str.format(self.template, **self.props)

    def construct_url(self):
        return self.get_base_url() + self.drs_base_path + self.format_endpoint()

    def construct_headers(self):
        headers = {}
        if self.authtoken:
            headers["Authorization"] = "Bearer " + self.authtoken
        return headers

    def construct_params(self):
        return {}

    def construct_request(self):
        url = self.construct_url()
        headers = self.construct_headers()
        params = self.construct_params()

        return [url, headers, params]

    def issue_request(self):

        url, headers, params = self.construct_request()
        gl.logger.debug("URL: " + url)
        gl.logger.debug("Headers: " + str(sanitize(headers)))
        gl.logger.debug("Request params: " + str(sanitize(params)))

        try:
            return requests.get(url, headers=headers, params=params,
                verify=self.ssl_verify)
        except requests.exceptions.SSLError as e:
            raise drs_exceptions.SSLException(str(e))
    
    def set_base_url(self, base_url):
        self.props["base_url"] = base_url
    
    def get_base_url(self):
        return self.props["base_url"]

    def set_object_id(self, object_id):
        self.props["object_id"] = object_id
    
    def get_object_id(self):
        return self.props["object_id"]
