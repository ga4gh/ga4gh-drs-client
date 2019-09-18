class GlobalState(object):

    def __init__(self):
        self.props = {}
    
    def set_prop(self, key, value):
        self.props[key] = value
    
    def get_prop(self, key):
        return self.props[key]

GLOBALSTATE = GlobalState()
