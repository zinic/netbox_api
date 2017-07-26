import unittest

from netbox_api.api import new_api_client
from netbox_api.model import *


class WhenRequesting(unittest.TestCase):
    def setUp(self):
        self.netbox = new_api_client(
            host='192.168.13.70',
            port=8080,
            scheme='http',
            token='1cc26306d45f980332484221d42e5beab7bc3aaa')

    def tearDown(self):
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


if __name__ == '__main__':
    unittest.main()
