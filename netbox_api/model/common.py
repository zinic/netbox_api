class CustomFields(object):
    def __init__(self, fields=None):
        self.fields = fields

    def items(self):
        return self.fields.items()

    def get(self, item, default=None):
        return self.fields.get(item, default)

    def __getitem__(self, item):
        return self.fields[item]

    @classmethod
    def from_dict(cls, contents):
        if contents is None:
            return cls()

        return cls(contents)
