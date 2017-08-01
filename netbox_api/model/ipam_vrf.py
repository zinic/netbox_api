from netbox_api.model.common import CustomFields


class VRFTenant(object):
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


class VRF(object):
    def __init__(self, tenant=None, custom_fields=None, id=None, name=None, rd=None, enforce_unique=None,
                 description=None, display_name=None):
        self.tenant = VRFTenant.from_dict(tenant)
        self.custom_fields = CustomFields.from_dict(custom_fields)
        self.id = id
        self.name = name
        self.rd = rd
        self.enforce_unique = enforce_unique
        self.description = description
        self.display_name = display_name

    @classmethod
    def from_dict(cls, contents):
        if contents is None:
            return cls()

        return cls(**contents)
