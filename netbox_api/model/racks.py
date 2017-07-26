from netbox_api.model.common import CustomFields
from enum import Enum


class RackWidthConstant(Enum):
    WIDTH_19_INCHES = 19
    WIDTH_23_INCHES = 23


class RackTypeConstant(Enum):
    FRAME_2_POST = 100
    FRAME_4_POST = 200
    CABINET_4_POST = 300
    FRAME_WALL_MOUNTED = 1000
    CABINET_WALL_MOUNTED = 1100


class RackSite(object):
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


class RackGroup(object):
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


class RackTenant(object):
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


class RackRole(object):
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


class RackType(object):
    def __init__(self, value=None, label=None):
        self.value = value
        self.label = label

    @classmethod
    def from_dict(cls, contents):
        if contents is None:
            return cls()

        return cls(**contents)


class RackWidth(object):
    def __init__(self, value=None, label=None):
        self.value = value
        self.label = label

    @classmethod
    def from_dict(cls, contents):
        if contents is None:
            return cls()

        return cls(**contents)


class Rack(object):
    def __init__(self, site=None, group=None, tenant=None, role=None, type=None, width=None, custom_fields=None,
                 id=None, name=None, facility_id=None, display_name=None, u_height=None, desc_units=None,
                 comments=None):
        self.site = RackSite.from_dict(site)
        self.group = RackGroup.from_dict(group)
        self.tenant = RackTenant.from_dict(tenant)
        self.role = RackRole.from_dict(role)
        self.type = RackType.from_dict(type)
        self.width = RackWidth.from_dict(width)
        self.custom_fields = CustomFields.from_dict(custom_fields)
        self.id = id
        self.name = name
        self.facility_id = facility_id
        self.display_name = display_name
        self.u_height = u_height
        self.desc_units = desc_units
        self.comments = comments

    @classmethod
    def from_dict(cls, contents):
        if contents is None:
            return cls()

        return cls(**contents)
