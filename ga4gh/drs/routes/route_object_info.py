from ga4gh.drs.routes.route import Route

class RouteObjectInfo(Route):

    def __init__(self, base_url, object_id, expand, suppress_ssl_verify=False,
        authtoken=None):

        super(RouteObjectInfo, self).__init__(base_url, object_id, 
            suppress_ssl_verify=suppress_ssl_verify, authtoken=authtoken)
        self.set_expand(expand)
        self.template = "/objects/{object_id}"

    def construct_params(self):
        return {"expand": self.get_expand()}
    
    def set_expand(self, expand):
        self.props["expand"] = expand
    
    def get_expand(self):
        return self.props["expand"]