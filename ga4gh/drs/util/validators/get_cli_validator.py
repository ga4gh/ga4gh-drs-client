from ga4gh.drs.exceptions.drs_exceptions import CLIException
from urllib.parse import urlparse

class GetCliValidator(object):

    def __init__(self, **kwargs):
        self.props = {k: kwargs[k] for k in kwargs.keys()}

    def validate_args(self):

        url = self.get_property("url")
        object_id = self.get_property("object_id")
        
        mandatory = [{"desc": "url", "value": url},
                     {"desc": "object id", "value": object_id}]

        for option in mandatory:
            if not option["value"]:
                raise CLIException("No %s specified" % (option["desc"]))

        parsed_url = urlparse(url)
        if parsed_url.scheme != "https":
            raise CLIException("Invalid URL scheme. Only https supported")
        if parsed_url.netloc == "":
            raise CLIException("Invalid URL provided")
    
    def set_property(self, key, value):
        self.props[key] = value
    
    def get_property(self, key):
        return self.props[key]
