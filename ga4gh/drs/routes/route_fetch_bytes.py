from ga4gh.drs.routes.route import Route

class RouteFetchBytes(Route):

    def __init__(self, base_url, object_id, access_id):
        super(RouteFetchBytes, self).__init__(base_url, object_id)
        self.access_id = access_id
        self.set_access_id(access_id)
        self.template = "/objects/{object_id}/access/{access_id}"
    
    def set_access_id(self, access_id):
        self.props["access_id"] = access_id
    
    def get_access_id(self):
        return self.props["access_id"]