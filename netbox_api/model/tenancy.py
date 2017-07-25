from netbox_api.model.common import CustomFields


class Group(object):
    def __init__(self, id=None, url=None, name=None, slug=None):
        self.id = id
        self.url = url
        self.name = name
        self.slug = slug

    @classmethod
    def from_dict(cls, contents):
        if contents is None:
            return cls()

        return cls(**contents)


class Tenant(object):
    def __init__(self, group=None, custom_fields=None, id=None, name=None, slug=None, description=None, comments=None):
        self.group = Group.from_dict(group)
        self.custom_fields = CustomFields.from_dict(custom_fields)
        self.id = id
        self.name = name
        self.slug = slug
        self.description = description
        self.comments = comments

    @classmethod
    def from_dict(cls, contents):
        if contents is None:
            return cls()

        return cls(**contents)
