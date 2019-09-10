# -*- coding: utf-8 -*-
"""Module ga4gh.drs.definitions.access_url.py
Contains class representation of "6.2 AccessURL" object outlined in DRS 
specification. Contains url to download requested object, as well as required
headers for authentication/authorization
"""

import requests

class AccessUrl(object):
    """Contains URL and auth headers needed to downloaded requested DRS object

    Attributes:
        json (dict): parsed AccessURL JSON, used to set other attributes
        access_method (AccessMethod): reference to parent AccessMethod
        headers (dict): auth headers required to make the download request
        url (str): fully resolvable URL that can be used to fetch object bytes
    """
    
    def __init__(self, json, access_method):
        """Instantiates an AccessUrl object

        Arguments:
            json (dict): parsed AccessUrl JSON
            access_method (AccessMethod): reference to parent AccessMethod obj
        """

        self.json = json
        self.access_method = access_method
        self.headers = self.__initialize_headers()
        self.url = self.__initialize_url()

    def issue_request(self):
        """Makes request to the specified url using associated headers"""

        drs_obj = self.access_method.drs_obj
        suppress_ssl_verify = drs_obj.cli_kwargs["suppress_ssl_verify"]
        verify = not suppress_ssl_verify

        return requests.get(self.url, headers=self.headers, verify=verify)

    def __initialize_headers(self):
        """Initializes value of headers property

        Returns:
            (dict): auth headers to make request
        """

        return self.json["headers"] if "headers" in self.json.keys() else {}
    
    def __initialize_url(self):
        """Initializes value of url property

        Returns:
            (str): url to make the request
        """

        return self.json["url"]

    def set_url(self, url):
        """Set the url property

        Arguments:
            url (str): url to set as AccessUrl url property
        """

        self.url = url
    
    def set_headers(self, headers):
        """Set the headers property

        Arguments:
            headers (dict): headers dict to set as AccessUrl headers property
        """

        self.headers = headers

    def get_url(self):
        """Retrieve AccessUrl url property

        Returns:
            (str): url
        """

        return self.url
    
    def get_headers(self):
        """Retrieve AccessUrl headers property

        Returns:
            (dict): headers
        """

        return self.headers
