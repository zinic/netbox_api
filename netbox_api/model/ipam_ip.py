from netbox_api.model.common import CustomFields
from enum import Enum


class IPAddressStatusConstant(Enum):
    ACTIVE = 1
    RESERVED = 2
    DEPRECATED = 3
    DHCP = 5


class IPAddressRoleConstant(Enum):
    LOOPBACK = 10
    SECONDARY = 20
    ANYCAST = 30
    VIP = 40
    VRRP = 41
    HSRP = 42
    GLBP = 43


class VRF(object):
    def __init__(self, id=None, url=None, name=None, rd=None):
        self.id = id
        self.url = url
        self.name = name
        self.rd = rd

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


class Status(object):
    def __init__(self, label=None, value=None):
        self.label = label
        self.value = value

    @classmethod
    def from_dict(cls, contents):
        if contents is None:
            return cls()

        return cls(**contents)


class Role(object):
    def __init__(self, label=None, value=None):
        self.label = label
        self.value = value

    @classmethod
    def from_dict(cls, contents):
        if contents is None:
            return cls()

        return cls(**contents)


class Device(object):
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


class FormFactor(object):
    def __init__(self, label=None, value=None):
        self.label = label
        self.value = value

    @classmethod
    def from_dict(cls, contents):
        if contents is None:
            return cls()

        return cls(**contents)


class Interface(object):
    def __init__(self, device=None, form_factor=None, id=None, name=None, enabled=None, lag=None, mtu=None,
                 mac_address=None, mgmt_only=None, description=None, is_connected=None, interface_connection=None,
                 circuit_termination=None):
        self.device = Device.from_dict(device)
        self.form_factor = FormFactor.from_dict(form_factor)
        self.id = id
        self.name = name
        self.enabled = enabled
        self.lag = lag
        self.mtu = mtu
        self.mac_address = mac_address
        self.mgmt_only = mgmt_only
        self.description = description
        self.is_connected = is_connected
        self.interface_connection = interface_connection
        self.circuit_termination = circuit_termination

    @classmethod
    def from_dict(cls, contents):
        if contents is None:
            return cls()

        return cls(**contents)


class IPAddress(object):
    def __init__(self, vrf=None, tenant=None, status=None, role=None, interface=None, custom_fields=None, id=None,
                 family=None, address=None, description=None, nat_inside=None, nat_outside=None):
        self.vrf = VRF.from_dict(vrf)
        self.tenant = Tenant.from_dict(tenant)
        self.status = Status.from_dict(status)
        self.role = Role.from_dict(role)
        self.interface = Interface.from_dict(interface)
        self.custom_fields = CustomFields.from_dict(custom_fields)
        self.id = id
        self.family = family
        self.address = address
        self.description = description
        self.nat_inside = nat_inside
        self.nat_outside = nat_outside

    @classmethod
    def from_dict(cls, contents):
        if contents is None:
            return cls()

        return cls(**contents)
