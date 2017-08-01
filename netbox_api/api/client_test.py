import unittest
import traceback

from netbox_api.api import new_api_client
from netbox_api.model import *

import random
import string

_SLUG_SUFFIX = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(4))


def _unique(name):
    return '{}_{}'.format(name, _SLUG_SUFFIX)


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
        except Exception as ex:
            print(ex)
            traceback.print_exc()

        self.netbox.ipam_delete_ip_address(self.device_ip_address.id)
        self.netbox.ipam_delete_ip_address(self.device_nat_ip.id)
        self.netbox.ipam_delete_vrf(self.vrf.id)
        self.netbox.ipam_delete_prefix_role(self.ipam_prefix_role.id)

        self.netbox.delete_interface(self.device_interface.id)
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
            name=_unique('tenant_group_test'),
            slug=_unique('tenant_group_test'))
        self.tenant_group = self.netbox.tenant_group(tenant_group_id)

        tenant_id = self.netbox.create_tenant(
            name=_unique('tenant_test'),
            slug=_unique('tenant_test'),
            tenant_group_id=tenant_group_id,
            description='test',
            comments='test')
        self.tenant = self.netbox.tenant(tenant_id)

        # Regions
        region_id = self.netbox.create_region(
            name=_unique('test_region'),
            slug=_unique('test_region'))
        self.region = self.netbox.region(region_id)

        # Sites
        site_id = self.netbox.create_site(
            name=_unique('test_site'),
            slug=_unique('test_site'),
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
            name=_unique('test_rack_role'),
            slug=_unique('test_rack_role'),
            color='fefefe')
        self.rack_role = self.netbox.rack_role(rack_role_id)

        rack_group_id = self.netbox.create_rack_group(
            name=_unique('test_rack_group'),
            slug=_unique('test_rack_group'),
            site_id=site_id)
        self.rack_group = self.netbox.rack_group(rack_group_id)

        rack_id = self.netbox.create_rack(
            name=_unique('test_rack'),
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
            name=_unique('test_device_role'),
            slug=_unique('test_device_role'),
            color='fefefe')
        self.device_role = self.netbox.device_role(device_role_id)

        manufacturer_id = self.netbox.create_manufacturer(
            name=_unique('test_manufacturer'),
            slug=_unique('test_manufacturer'))
        self.manufacturer = self.netbox.manufacturer(manufacturer_id)

        platform_id = self.netbox.create_platform(
            name=_unique('test_platform'),
            slug=_unique('test_platform'))
        self.platform = self.netbox.platform(platform_id)

        device_type_id = self.netbox.create_device_type(
            model=_unique('test_model'),
            slug=_unique('test_model'),
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

        device_id = self.netbox.create_device(
            name=_unique('test_device'),
            device_role_id=self.device_role.id,
            status=DeviceStatusConstant.ACTIVE,
            site_id=self.site.id,
            rack_face=RackFaceConstant.FRONT,
            asset_tag=_unique('12345'),
            platform_id=self.platform.id,
            # primary_ip4_id='192.168.1.1',
            # primary_ip6_id='2001:db8:85a3::8a2e:370:7334',
            position=1,
            device_type_id=self.device_type.id,
            serial=_unique('54321'),
            rack_id=self.rack.id,
            tenant_id=self.tenant.id)
        self.device = self.netbox.device(device_id)

        device_interface_id = self.netbox.create_interface(
            name=_unique('test_interface'),
            form_factor=FormFactorConstant.BASE_T_1GE,
            device_id=self.device.id,
            mac_address='aa:aa:aa:aa:aa:aa',
            management_only=False)
        self.device_interface = self.netbox.interface(device_interface_id)

        # IPAM
        prefix_role_id = self.netbox.ipam_create_prefix_role(
            name=_unique('test_ipam_role'),
            slug=_unique('test_ipam_role'),
            weight=1)
        self.ipam_prefix_role = self.netbox.ipam_prefix_role(prefix_role_id)

        vrf_id = self.netbox.ipam_create_vrf(
            name=_unique('test_vrf'),
            route_distinguisher='65000:10',
            tenant_id=tenant_id,
            enforce_unique=False,
            description='test')

        self.vrf = self.netbox.ipam_vrf(vrf_id)

        nat_ip_id = self.netbox.ipam_create_ip_address(
            address='10.2.1.1',
            status=IPAddressStatusConstant.ACTIVE,
            tenant_id=self.tenant.id,
            description='test')
        self.device_nat_ip = self.netbox.ipam_ip_address(nat_ip_id)

        ip_id = self.netbox.ipam_create_ip_address(
            address='10.1.1.1',
            status=IPAddressStatusConstant.ACTIVE,
            role=IPAddressRoleConstant.ANYCAST,
            interface_id=self.device_interface.id,
            tenant_id=self.tenant.id,
            vrf_id=self.vrf.id,
            nat_inside=None,
            description='test')
        self.device_ip_address = self.netbox.ipam_ip_address(ip_id)

        try:
            pass
        except Exception as ex:
            print(ex)
            traceback.print_exc()


if __name__ == '__main__':
    unittest.main()
