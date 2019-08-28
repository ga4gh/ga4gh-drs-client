# -*- coding: utf-8 -*-
"""Module ga4gh.drs.routes.route_object_info.py
Contains the RouteObjectInfo class, which makes the request to the 
'/objects/{object_id}' route outlined in the DRS specification.
"""

from ga4gh.drs.routes.route import Route

class RouteObjectInfo(Route):
    """Makes request to the '/objects/{object_id}' route in DRS specification

    Attributes:
        expand (bool): sent as query parameter in the request to expand bundles
        template (str): object info route endpoint template
    """

    def __init__(self, base_url, object_id, expand, suppress_ssl_verify=False,
        authtoken=None):
        """Instantiates a RouteObjectInfo object

        Arguments:
            base_url (str): base url to DRS service (excludes DRS base path)
            object_id (str): id of requested DRS object
            expand (bool): if True, request that bundles be expanded
            suppress_ssl_verify (bool): if True, skip ssl verification
            authtoken (str): OAuth 2.0 access token
        """

        super(RouteObjectInfo, self).__init__(base_url, object_id, 
            suppress_ssl_verify=suppress_ssl_verify, authtoken=authtoken)
        self.set_expand(expand)
        self.template = "/objects/{object_id}"

    def construct_params(self):
        """Construct query parameters necessary to make successful request

        Returns:
            (dict): request query parameters
        """

        return {"expand": self.get_expand()}
    
    def set_expand(self, expand):
        """Set the route's 'expand' query parameter property

        Arguments:
            expand (bool): if True, request that bundles be expanded
        """

        self.props["expand"] = expand
    
    def get_expand(self):
        """Retrieve the route's 'expand' query parameter property

        Returns:
            (bool): expand property
        """

        return self.props["expand"]