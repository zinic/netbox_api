class DeviceRole(object):
    def __init__(self, id=None, name=None, slug=None, color=None):
        self.id = id
        self.name = name
        self.slug = slug
        self.color = color

    @classmethod
    def from_dict(cls, contents):
        if contents is None:
            return cls()

        return cls(**contents)
