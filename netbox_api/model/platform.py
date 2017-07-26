class Platform(object):
    def __init__(self, id=None, name=None, slug=None, napalm_driver=None, rpc_client=None):
        self.id = id
        self.name = name
        self.slug = slug
        self.napalm_driver = napalm_driver
        self.rpc_client = rpc_client

    @classmethod
    def from_dict(cls, contents):
        if contents is None:
            return cls()

        return cls(**contents)
