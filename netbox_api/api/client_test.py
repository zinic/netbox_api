import unittest

from netbox_api.api import new_api_client


class WhenRequesting(unittest.TestCase):
    def test_get_device(self):
        netbox = new_api_client()

        netbox.device(1)
        netbox.lookup_device('r101u1')

        # netbox.list_devices(cf_Tags='elasticsearch')
        # netbox.update_device_custom_fields(203, {
        #     'Tags': 'elasticsearch,master_node,event-service-v2'
        # })

    def test_get_site(self):
        netbox = new_api_client()

        netbox.site(2)
        netbox.lookup_site('SE2')

    def test_get_tenant(self):
        netbox = new_api_client()

        netbox.tenant(1)
        netbox.lookup_tenant('Infrastructure')

    def test_get_interface(self):
        netbox = new_api_client()

        netbox.interface(4513)
        netbox.lookup_device_interface('r113u2', 'p2p1')
        netbox.lookup_device_interfaces('r113u2')

        print(netbox.create_interface('test', 800, 1, mac_address='aa:aa:aa:aa:aa:aa'))


if __name__ == '__main__':
    unittest.main()
