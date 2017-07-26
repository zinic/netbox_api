class Manufacturer(object):
    def __init__(self, id=None, name=None, slug=None):
        self.id = id
        self.name = name
        self.slug = slug

    @classmethod
    def from_dict(cls, contents):
        if contents is None:
            return cls()

        return cls(**contents)
