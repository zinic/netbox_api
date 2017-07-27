import unittest

from netbox_api.api import new_api_client
from netbox_api.model import *


class WhenRequesting(unittest.TestCase):
    def setUp(self):
        self.netbox = new_api_client(
            host='localhost',
            port=8080,
            scheme='http',
            token='token')

    def tearDown(self):
        try:
            pass
        except Exception:
            pass

        self.netbox.delete_device(self.device.id)
        self.netbox.delete_device_type(self.device_type.id)
        self.netbox.delete_platform(self.platform.id)
        self.netbox.delete_manufacturer(self.manufacturer.id)
        self.netbox.delete_device_role(self.device_role.id)
        self.netbox.delete_rack(self.rack.id)
        self.netbox.delete_rack_group(self.rack_group.id)
        self.netbox.delete_rack_role(self.rack_role.id)
        self.netbox.delete_site(self.site.id)
        self.netbox.delete_region(self.region.id)
        self.netbox.delete_tenant(self.tenant.id)
        self.netbox.delete_tenant_group(self.tenant_group.id)

    def test_all(self):
        # Tenants
        tenant_group_id = self.netbox.create_tenant_group(
            name='tenant_group_test',
            slug='tenant_group_test')
        self.tenant_group = self.netbox.tenant_group(tenant_group_id)

        tenant_id = self.netbox.create_tenant(
            name='tenant_test',
            slug='tenant_test',
            tenant_group_id=tenant_group_id,
            description='test',
            comments='test')
        self.tenant = self.netbox.tenant(tenant_id)

        # Regions
        region_id = self.netbox.create_region(
            name='test_region',
            slug='test_region')
        self.region = self.netbox.region(region_id)

        # Sites
        site_id = self.netbox.create_site(
            name='test_site',
            slug='test_site',
            tenant_id=tenant_id,
            region_id=region_id,
            facility='DC1',
            contact_email='test@example.com',
            physical_address='1245 South Rd. Unit 002, Austin TX, 73301',
            shipping_address='1245 South Rd. Unit 002, Austin TX, 73301',
            contact_name='myname',
            contact_phone='1-555-555-5555',
            asn=1212,
            comments='test')
        self.site = self.netbox.site(site_id)

        # Racks
        rack_role_id = self.netbox.create_rack_role(
            name='test_rack_role',
            slug='test_rack_role',
            color='fefefe')
        self.rack_role = self.netbox.rack_role(rack_role_id)

        rack_group_id = self.netbox.create_rack_group(
            name='test_rack_group',
            slug='test_rack_group',
            site_id=site_id)
        self.rack_group = self.netbox.rack_group(rack_group_id)

        rack_id = self.netbox.create_rack(
            name='test_rack',
            rack_group_id=self.rack_group.id,
            rack_role_id=self.rack_role.id,
            site_id=self.site.id,
            tenant_id=self.tenant.id,
            u_height=48,
            width=RackWidthConstant.WIDTH_23_INCHES,
            facility='DC1',
            descending_units=False,
            rack_type=RackTypeConstant.CABINET_4_POST)
        self.rack = self.netbox.rack(rack_id)

        # Devices
        device_role_id = self.netbox.create_device_role(
            name='test_device_role',
            slug='test_device_role',
            color='fefefe')
        self.device_role = self.netbox.device_role(device_role_id)

        manufacturer_id = self.netbox.create_manufacturer(
            name='test_manufacturer',
            slug='test_manufacturer')
        self.manufacturer = self.netbox.manufacturer(manufacturer_id)

        platform_id = self.netbox.create_platform(
            name='test_platform',
            slug='test_platform')
        self.platform = self.netbox.platform(platform_id)

        device_type_id = self.netbox.create_device_type(
            model='test_model',
            slug='test_model',
            u_height=1,
            subdevice_role=SubdeviceTypeConstant.NONE,
            manufacturer_id=manufacturer_id,
            part_number='12345abcde',
            interface_ordering=InterfaceOrderConstant.BY_RACK_POSITION,
            is_pdu=False,
            is_console_server=False,
            is_full_depth=True,
            is_network_device=False)
        self.device_type = self.netbox.device_type(device_type_id)

        try:
            device_id = self.netbox.create_device(
                name='test_device',
                device_role_id=self.device_role.id,
                status=DeviceStatusConstant.ACTIVE,
                site_id=self.site.id,
                rack_face=RackFaceConstant.FRONT,
                asset_tag='12345',
                platform_id=self.platform.id,
                # primary_ip4_id='192.168.1.1',
                # primary_ip6_id='2001:db8:85a3::8a2e:370:7334',
                position=1,
                device_type_id=self.device_type.id,
                serial='54321',
                rack_id=self.rack.id,
                tenant_id=self.tenant.id)
            self.device = self.netbox.device(device_id)
        except Exception as ex:
            print(ex)


if __name__ == '__main__':
    unittest.main()
