from netbox_api.model.common import CustomFields


class SiteTenant(object):
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


class Site(object):
    def __init__(self, tenant=None, custom_fields=None, id=None, name=None, slug=None, region=None, facility=None,
                 asn=None, physical_address=None, shipping_address=None, contact_name=None, contact_phone=None,
                 contact_email=None, comments=None, count_prefixes=None, count_vlans=None, count_racks=None,
                 count_devices=None, count_circuits=None):
        self.tenant = SiteTenant.from_dict(tenant)
        self.custom_fields = CustomFields.from_dict(custom_fields)
        self.id = id
        self.name = name
        self.slug = slug
        self.region = region
        self.facility = facility
        self.asn = asn
        self.physical_address = physical_address
        self.shipping_address = shipping_address
        self.contact_name = contact_name
        self.contact_phone = contact_phone
        self.contact_email = contact_email
        self.comments = comments
        self.count_prefixes = count_prefixes
        self.count_vlans = count_vlans
        self.count_racks = count_racks
        self.count_devices = count_devices
        self.count_circuits = count_circuits

    @classmethod
    def from_dict(cls, contents):
        if contents is None:
            return cls()

        return cls(**contents)
