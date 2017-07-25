from netbox_api.model.common import CustomFields


class Manufacturer(object):
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


class DeviceType(object):
    def __init__(self, manufacturer=None, id=None, url=None, model=None, slug=None):
        self.manufacturer = Manufacturer.from_dict(manufacturer)
        self.id = id
        self.url = url
        self.model = model
        self.slug = slug

    @classmethod
    def from_dict(cls, contents):
        if contents is None:
            return cls()

        return cls(**contents)


class DeviceRole(object):
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


class Platform(object):
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


class DeviceSite(object):
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


class Rack(object):
    def __init__(self, id=None, url=None, name=None, display_name=None):
        self.id = id
        self.url = url
        self.name = name
        self.display_name = display_name

    @classmethod
    def from_dict(cls, contents):
        if contents is None:
            return cls()

        return cls(**contents)


class Face(object):
    def __init__(self, value=None, label=None):
        self.value = value
        self.label = label

    @classmethod
    def from_dict(cls, contents):
        if contents is None:
            return cls()

        return cls(**contents)


class Status(object):
    def __init__(self, value=None, label=None):
        self.value = value
        self.label = label

    @classmethod
    def from_dict(cls, contents):
        if contents is None:
            return cls()

        return cls(**contents)


class PrimaryIp(object):
    def __init__(self, id=None, url=None, family=None, address=None):
        self.id = id
        self.url = url
        self.family = family
        self.address = address

    @classmethod
    def from_dict(cls, contents):
        if contents is None:
            return cls()

        return cls(**contents)


class PrimaryIp4(object):
    def __init__(self, id=None, url=None, family=None, address=None):
        self.id = id
        self.url = url
        self.family = family
        self.address = address

    @classmethod
    def from_dict(cls, contents):
        if contents is None:
            return cls()

        return cls(**contents)


class Device(object):
    def __init__(self, device_type=None, device_role=None, tenant=None, platform=None, site=None, rack=None, face=None,
                 status=None, primary_ip=None, primary_ip4=None, custom_fields=None, id=None, name=None,
                 display_name=None, serial=None, asset_tag=None, position=None, parent_device=None, primary_ip6=None,
                 comments=None):
        self.device_type = DeviceType.from_dict(device_type)
        self.device_role = DeviceRole.from_dict(device_role)
        self.tenant = Tenant.from_dict(tenant)
        self.platform = Platform.from_dict(platform)
        self.site = DeviceSite.from_dict(site)
        self.rack = Rack.from_dict(rack)
        self.face = Face.from_dict(face)
        self.status = Status.from_dict(status)
        self.primary_ip = PrimaryIp.from_dict(primary_ip)
        self.primary_ip4 = PrimaryIp4.from_dict(primary_ip4)
        self.custom_fields = CustomFields.from_dict(custom_fields)
        self.id = id
        self.name = name
        self.display_name = display_name
        self.serial = serial
        self.asset_tag = asset_tag
        self.position = position
        self.parent_device = parent_device
        self.primary_ip6 = primary_ip6
        self.comments = comments

    @classmethod
    def from_dict(cls, contents):
        if contents is None:
            return cls()

        return cls(**contents)
