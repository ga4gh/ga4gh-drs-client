# -*- coding: utf-8 -*-
"""Module ga4gh.drs.util.validators.get_cli_validator.py
Validates command-line input for the 'drs get' command (beyond what is 
provided by default from Click)
"""

import os
from ga4gh.drs.exceptions.drs_exceptions import CLIException
from urllib.parse import urlparse

class GetCliValidator(object):
    """Validate command-line input for 'drs get' command

    Attributes:
        props (dict): cli properties dictionary
    """

    def __init__(self, **kwargs):
        """Instantiates a GetCliValidator object

        Arguments:
            kwargs (dict): command-line arguments/options
        """

        self.props = {k: kwargs[k] for k in kwargs.keys()}
    
    def validate_all(self):
        self.validate_args()
        self.validate_url()
        self.validate_output_dirs()
    
    def validate_args(self):
        """Validate supplied command-line arguments are acceptable

        Raises:
            CLIException: raised if an issue with one or more args is found
        """

        url = self.get_property("url")
        object_id = self.get_property("object_id")
        
        mandatory = [{"desc": "url", "value": url},
                     {"desc": "object id", "value": object_id}]

        # validates that all mandatory arguments have been supplied and are
        # present in the kwargs dictionary
        for option in mandatory:
            if not option["value"]:
                raise CLIException("No %s specified" % (option["desc"]))

    def validate_url(self):
        """Assert the url cli argument is valid

        Raises:
            CLIException: raised if an issue with url is found
        """

        url = self.get_property("url")
        # parse the url under the 'url' property. Url must have a scheme
        # of "https," and must have a netloc that is not null/empty
        parsed_url = urlparse(url)
        if parsed_url.scheme != "https":
            raise CLIException("Invalid URL scheme. Only https supported")
        if parsed_url.netloc == "":
            raise CLIException("Invalid URL provided")
    
    def validate_output_dirs(self):
        """Validate output directories exist

        Raises:
            CLIException: raised if an output directory is found to not exist
        """

        output_dir = os.path.join(self.get_property("output_dir"), '') \
                     if "output_dir" in self.props.keys() else "."
        metadata_dir = os.path.dirname(self.get_property("output_metadata")) \
                       if self.get_property("output_metadata") else None
        log_dir = os.path.dirname(self.get_property("logfile")) \
                  if self.get_property("logfile") else None

        dirs = [output_dir, metadata_dir, log_dir]

        for d in dirs:
            if d:
                if not os.path.exists(d):
                    raise CLIException("Output directory: " + d + " does not "
                                       "exist")

    def set_property(self, key, value):
        """Set a key, value property

        Arguments:
            key (str): property key
            value (object): property value
        """

        self.props[key] = value
    
    def get_property(self, key):
        """Get the value of a key stored in the properties dictionary

        Arguments:
            key (str): property key

        Returns:
            (object): stored value in properties dict under key
        """

        return self.props[key]
