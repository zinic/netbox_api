class CustomFields(object):
    def __init__(self, tags=None):
        self.tags = tags

    @classmethod
    def from_dict(cls, contents):
        if contents is None:
            return cls()

        if 'Tags' in contents:
            contents['tags'] = contents['Tags']
            del contents['Tags']

        return cls(**contents)
