class PrefixRole(object):
    def __init__(self, id=None, name=None, slug=None, weight=None):
        self.id = id
        self.name = name
        self.slug = slug
        self.weight = weight

    @classmethod
    def from_dict(cls, contents):
        if contents is None:
            return cls()

        return cls(**contents)
