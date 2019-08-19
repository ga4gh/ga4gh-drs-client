from ga4gh.drs.routes.route import Route

class RouteObjectInfo(Route):

    def __init__(self, base_url, object_id, expand):
        super(RouteObjectInfo, self).__init__(base_url, object_id)
        self.set_expand(expand)
        self.template = "/objects/{object_id}"

    def construct_request(self):
        url = self.full_url()
        headers = {}
        params = {"expand": self.get_expand()}

        return [url, headers, params]
    
    def set_expand(self, expand):
        self.props["expand"] = expand
    
    def get_expand(self):
        return self.props["expand"]