# -*- coding: utf-8 -*-
"""Module ga4gh.drs.routes.route_fetch_bytes.py
Contains the RouteFetchBytes class, which makes the request to the 
'/objects/{object_id}/access/{access_id}' route outlined in the DRS
specification.
"""

from ga4gh.drs.routes.route import Route

class RouteFetchBytes(Route):
    """Makes request to '/objects/{object_id}/access/{access_id}' route

    Attributes:
        template (str): fetch bytes route endpoint template
    """

    def __init__(self, base_url, object_id, access_id, 
        suppress_ssl_verify=False, authtoken=None):
        """Instantiates a RouteFetchBytes object

        Arguments:
            base_url (str): base url to DRS service (excludes DRS base path)
            object_id (str): id of requested DRS object
            access_id (str): access id of requested DRS object
        """

        super(RouteFetchBytes, self).__init__(base_url, object_id, 
            suppress_ssl_verify=suppress_ssl_verify, authtoken=authtoken)
        self.set_access_id(access_id)
        self.template = "/objects/{object_id}/access/{access_id}"
    
    def set_access_id(self, access_id):
        """Set the route's 'access_id' path parameter
        
        Arguments:
            access_id (str): access id of requested DRS object
        """

        self.props["access_id"] = access_id
    
    def get_access_id(self):
        """Retrieve the route's 'access_id' path parameter

        Returns:
            (str): DRS object access id
        """

        return self.props["access_id"]