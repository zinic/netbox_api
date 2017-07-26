class Region(object):
    def __init__(self, id=None, name=None, slug=None, parent=None):
        self.id = id
        self.name = name
        self.slug = slug
        self.parent = parent

    @classmethod
    def from_dict(cls, contents):
        if contents is None:
            return cls()

        return cls(**contents)
