from netbox_api.model.common import CustomFields


class DeviceTypeManufacturer(object):
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


class InterfaceOrdering(object):
    def __init__(self, label=None, value=None):
        self.label = label
        self.value = value

    @classmethod
    def from_dict(cls, contents):
        if contents is None:
            return cls()

        return cls(**contents)


class DeviceType(object):
    def __init__(self, manufacturer=None, interface_ordering=None, custom_fields=None, id=None, model=None, slug=None,
                 part_number=None, u_height=None, is_full_depth=None, is_console_server=None, is_pdu=None,
                 is_network_device=None, subdevice_role=None, comments=None, instance_count=None):
        self.manufacturer = DeviceTypeManufacturer.from_dict(manufacturer)
        self.interface_ordering = InterfaceOrdering.from_dict(interface_ordering)
        self.custom_fields = CustomFields.from_dict(custom_fields)
        self.id = id
        self.model = model
        self.slug = slug
        self.part_number = part_number
        self.u_height = u_height
        self.is_full_depth = is_full_depth
        self.is_console_server = is_console_server
        self.is_pdu = is_pdu
        self.is_network_device = is_network_device
        self.subdevice_role = subdevice_role
        self.comments = comments
        self.instance_count = instance_count

    @classmethod
    def from_dict(cls, contents):
        if contents is None:
            return cls()

        return cls(**contents)
