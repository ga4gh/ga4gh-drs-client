# -*- coding: utf-8 -*-
"""Module ga4gh.drs.routes.route.py
Contains the Route class, which is the parent for both expected routes outlined
in the DRS specification, namely, '/objects/{object_id}' and 
'/objects/{object_id}/access/{access_id}'. Abstract parent holds common 
properties and methods of each 
"""

import ga4gh.drs.config.constants as c
import requests
from ga4gh.drs.config.global_state import GLOBALSTATE
from ga4gh.drs.exceptions import drs_exceptions
from ga4gh.drs.util.functions.logging import *


class Route(object):
    """Abstract parent of expected routes outlined in the DRS specification

    Attributes:
        props (dict): all properties dictionary
        ssl_verify (bool): if True, perform SSL verification (default)
        authtoken (str): OAuth 2.0 access token
        drs_base_path (str): constant base path to DRS objects
        template (str): route endpoint template
    """

    def __init__(self, base_url, object_id, suppress_ssl_verify=False, 
        authtoken=None):
        """Instantiates a Route object

        Arguments:
            base_url (str): base url to DRS service (excludes DRS base path)
            object_id (str): id of requested DRS object
            suppress_ssl_verify (bool): if True, skip ssl verification
            authtoken (str): OAuth 2.0 access token
        """

        self.props = {}
        self.set_base_url(base_url)
        self.set_object_id(object_id)
        self.ssl_verify = not suppress_ssl_verify
        self.authtoken = authtoken
        self.drs_base_path = c.HTTPS_BASE_PATH
        self.template = "/"
    
    def format_endpoint(self):
        """Format request endpoint path by modifying template with props values

        Returns:
            (str): route template, formatted according to props values
        """

        return str.format(self.template, **self.props)

    def construct_url(self):
        """Construct full url (base url, base path, endpoint) for DRS object

        Returns:
            (str): full https url to access DRS object
        """

        return self.get_base_url() + self.drs_base_path + self.format_endpoint()

    def construct_headers(self):
        """Construct headers necessary to make successful request

        Returns:
            (dict): request headers
        """

        headers = {}
        if self.authtoken:
            headers["Authorization"] = "Bearer " + self.authtoken
        return headers

    def construct_params(self):
        """Construct query parameters necessary to make successful request

        Returns:
            (dict): request query parameters
        """

        return {}

    def construct_request(self):
        """Construct all components for a full request (url, headers, params)

        Returns:
            (list): url, headers (dict), params (dict)
        """

        url = self.construct_url()
        headers = self.construct_headers()
        params = self.construct_params()

        return [url, headers, params]

    def issue_request(self):
        """Issue the https request and return the response

        Returns:
            (requests.Response): response object from request
        """

        url, headers, params = self.construct_request()
        logger = GLOBALSTATE.get_prop("logger")
        logger.debug("URL: " + url)
        logger.debug("Headers: " + str(sanitize(headers)))
        logger.debug("Request params: " + str(sanitize(params)))

        try:
            return requests.get(url, headers=headers, params=params,
                verify=self.ssl_verify)
        except requests.exceptions.SSLError as e:
            raise drs_exceptions.SSLException(str(e))
    
    def set_base_url(self, base_url):
        """Set the route's base url

        Arguments:
           base_url (str): base url
        """

        self.props["base_url"] = base_url
    
    def get_base_url(self):
        """Retrieve the route's base url

        Returns:
            (str): base url
        """

        return self.props["base_url"]

    def set_object_id(self, object_id):
        """Set the route's requested object id

        Arguments:
            object_id (str): object id
        """

        self.props["object_id"] = object_id
    
    def get_object_id(self):
        """Retrieve the route's object id

        Returns:
            (str): object id
        """

        return self.props["object_id"]
