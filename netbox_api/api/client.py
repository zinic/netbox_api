from netbox_api.api.protocol import RequestHandler
from netbox_api.model import *


class NetboxClient(object):
    def __init__(self, host, port, token, scheme, verify=None):
        # Request handling
        self._request_handler = RequestHandler(host, port, token, scheme, verify)

        # Client parts
        self.ipam = IPAMClient(self._request_handler)
        self.dcim = DCIMClient(self._request_handler)
        self.tenancy = TenancyClient(self._request_handler)


class NetboxClientPart(object):
    def __init__(self, request_handler):
        self._request_handler = request_handler

    def _format_url(self, path_fmt, *parts):
        return self._request_handler.format_url(path_fmt, *parts)

    def _request(self, method, url, **kwargs):
        return self._request_handler.request(
            method=method,
            url=url,
            **kwargs)

    def _paginate(self, cls, method, url, **kwargs):
        return self._request_handler.paginate(
            cls=cls,
            method=method,
            url=url,
            **kwargs)

    def _list(self, cls, uri, query_params):
        itr = self._paginate(
            cls=cls,
            method='get',
            url=self._format_url(uri),
            params=query_params)

        # TODO: Expose this as an optimization for other components later
        return [r for r in itr]


class DCIMClient(NetboxClientPart):
    def interface(self, interface_id):
        """
        Get a device interface by the interface's ID.

        :param interface_id:
        :return:
        """
        resp = self._request(
            method='get',
            url=self._format_url('/dcim/interfaces/{}', interface_id))

        # Raise on bad status codes
        resp.raise_on_status()

        # If there are results, return them
        return resp.wrap_results(Interface)[0]

    def list_interfaces(self, **query):
        return self._list(Interface, '/dcim/interfaces', query)

    def create_interface(self, name, form_factor, device_id, mac_address=None, management_only=False, parent_lag=None):
        """
        Create a new device interface. The ID of the new interface is returned upon success.

        :param name:
        :param form_factor:
        :param device_id:
        :param mac_address:
        :param management_only:
        :param parent_lag:
        :return:
        """
        # Map constants
        if isinstance(form_factor, FormFactorConstant):
            form_factor = form_factor.value

        resp = self._request(
            method='post',
            url=self._format_url('/dcim/interfaces'),
            json={
                'name': name,
                'form_factor': form_factor,
                'mac_address': mac_address,
                'lag': parent_lag,
                'device': device_id,
                'mgmt_only': management_only
            })

        # Raise on bad status codes
        resp.raise_on_status()

        # Return the ID of the new interface
        return resp.results[0]['id']

    def delete_interface(self, interface_id):
        """
        Deletes a device interface by the interface's ID.

        :param interface_id:
        :return:
        """
        resp = self._request(
            method='delete',
            url=self._format_url('/dcim/interfaces/{}', interface_id))

        # Raise on bad status codes
        resp.raise_on_status()

    def connect_interfaces(self, status, interface_a_id, interface_b_id):
        """
        Connect two device interfaces and assign the connection a status.

        :param status:
        :param interface_a_id:
        :param interface_b_id:
        :return:
        """
        resp = self._request(
            method='post',
            url=self._format_url('/dcim/interface-connections'),
            json={
                'connection_status': status,
                'interface_a': interface_a_id,
                'interface_b': interface_b_id
            })

        # Raise on bad status codes
        resp.raise_on_status()

    def region(self, region_id):
        resp = self._request(
            method='get',
            url=self._format_url('/dcim/regions/{}', region_id))

        # Raise on bad status codes
        resp.raise_on_status()

        # If there are results, return them
        return resp.wrap_results(Region)[0]

    def list_interfaces(self, **query):
        return self._list(Region, '/dcim/regions', query)

    def create_region(self, name, slug, parent_region_id=None):
        resp = self._request(
            method='post',
            url=self._format_url('/dcim/regions'),
            json={
                'name': name,
                'slug': slug,
                'parent': parent_region_id
            })

        # Raise on bad status codes
        resp.raise_on_status()

        # Return the ID of the new interface
        return resp.results[0]['id']

    def delete_region(self, region_id):
        resp = self._request(
            method='delete',
            url=self._format_url('/dcim/regions/{}', region_id))

        # Raise on bad status codes
        resp.raise_on_status()

    def site(self, site_id):
        """
        Get a site by the site's ID.

        :param site_id:
        :return:
        """
        resp = self._request(
            method='get',
            url=self._format_url('/dcim/sites/{}', site_id))

        # Raise on bad status codes
        resp.raise_on_status()

        # If there are results, return them
        return resp.wrap_results(Site)[0]

    def list_sites(self, **query):
        return self._list(Site, '/dcim/sites', query)

    def create_site(self, name, slug, tenant_id, region_id, contact_email=None, physical_address=None,
                    shipping_address=None, contact_name=None, contact_phone=None, asn=None, comments=None,
                    facility=None, custom_fields=None):
        resp = self._request(
            method='post',
            url=self._format_url('/dcim/sites'),
            json={
                'name': name,
                'slug': slug,
                'facility': facility,
                'tenant': tenant_id,
                'region': region_id,
                'contact_name': contact_name,
                'contact_phone': contact_phone,
                'contact_email': contact_email,
                'physical_address': physical_address,
                'shipping_address': shipping_address,
                'comments': comments,
                'asn': asn,
                'custom_fields': custom_fields if custom_fields is not None else dict()
            })

        # Raise on bad status codes
        resp.raise_on_status()

        # Return the ID of the new interface
        return resp.results[0]['id']

    def delete_site(self, site_id):
        resp = self._request(
            method='delete',
            url=self._format_url('/dcim/sites/{}', site_id))

        # Raise on bad status codes
        resp.raise_on_status()

    def rack_group(self, rack_group_id):
        resp = self._request(
            method='get',
            url=self._format_url('/dcim/rack-groups/{}', rack_group_id))

        # Raise on bad status codes
        resp.raise_on_status()

        # If there are results, return them
        return resp.wrap_results(RackGroup)[0]

    def list_rack_groups(self, **query):
        return self._list(RackGroup, '/dcim/rack-groups', query)

    def create_rack_group(self, name, slug, site_id):
        resp = self._request(
            method='post',
            url=self._format_url('/dcim/rack-groups'),
            json={
                'name': name,
                'slug': slug,
                'site': site_id
            })

        # Raise on bad status codes
        resp.raise_on_status()

        # Return the ID of the new interface
        return resp.results[0]['id']

    def delete_rack_group(self, rack_group_id):
        resp = self._request(
            method='delete',
            url=self._format_url('/dcim/rack-groups/{}', rack_group_id))

        # Raise on bad status codes
        resp.raise_on_status()

    def rack_role(self, rack_role_id):
        resp = self._request(
            method='get',
            url=self._format_url('/dcim/rack-roles/{}', rack_role_id))

        # Raise on bad status codes
        resp.raise_on_status()

        # If there are results, return them
        return resp.wrap_results(RackRole)[0]

    def list_rack_roles(self, **query):
        return self._list(RackRole, '/dcim/rack-roles', query)

    def create_rack_role(self, name, slug, color='000000'):
        resp = self._request(
            method='post',
            url=self._format_url('/dcim/rack-roles'),
            json={
                'name': name,
                'slug': slug,
                'color': color
            })

        # Raise on bad status codes
        resp.raise_on_status()

        # Return the ID of the new interface
        return resp.results[0]['id']

    def delete_rack_role(self, rack_role_id):
        resp = self._request(
            method='delete',
            url=self._format_url('/dcim/rack-roles/{}', rack_role_id))

        # Raise on bad status codes
        resp.raise_on_status()

    def rack(self, rack_id):
        resp = self._request(
            method='get',
            url=self._format_url('/dcim/racks/{}', rack_id))

        # Raise on bad status codes
        resp.raise_on_status()

        # If there are results, return them
        return resp.wrap_results(Rack)[0]

    def list_racks(self, **query):
        return self._list(Rack, '/dcim/racks', query)

    def create_rack(self, name, rack_group_id, site_id, tenant_id, u_height, width, descending_units, rack_type,
                    rack_role_id=None, facility=None, comments='', custom_fields=None):
        # Map constants to their values for the API
        if isinstance(rack_type, RackTypeConstant):
            rack_type = rack_type.value
        if isinstance(width, RackWidthConstant):
            width = width.value

        resp = self._request(
            method='post',
            url=self._format_url('/dcim/racks'),
            json={
                'name': name,
                'u_height': u_height,
                'width': width,
                'group': rack_group_id,
                'site': site_id,
                'facility_id': facility,
                'role': rack_role_id,
                'desc_units': descending_units,
                'type': rack_type,
                'tenant': tenant_id,
                'comments': comments,
                'custom_fields': custom_fields if custom_fields is not None else dict()
            })

        # Raise on bad status codes
        resp.raise_on_status()

        # Return the ID of the new interface
        return resp.results[0]['id']

    def delete_rack(self, rack_id):
        resp = self._request(
            method='delete',
            url=self._format_url('/dcim/racks/{}', rack_id))

        # Raise on bad status codes
        resp.raise_on_status()

    def platform(self, platform_id):
        resp = self._request(
            method='get',
            url=self._format_url('/dcim/platforms/{}', platform_id))

        # Raise on bad status codes
        resp.raise_on_status()

        # If there are results, return them
        return resp.wrap_results(Platform)[0]

    def create_platform(self, name, slug, rpc_client=''):
        resp = self._request(
            method='post',
            url=self._format_url('/dcim/platforms'),
            json={
                'name': name,
                'slug': slug,
                'rpc_client': rpc_client
            })

        # Raise on bad status codes
        resp.raise_on_status()

        # Return the ID of the new interface
        return resp.results[0]['id']

    def delete_platform(self, platform_id):
        resp = self._request(
            method='delete',
            url=self._format_url('/dcim/platforms/{}', platform_id))

        # Raise on bad status codes
        resp.raise_on_status()

    def manufacturer(self, manufacturer_id):
        resp = self._request(
            method='get',
            url=self._format_url('/dcim/manufacturers/{}', manufacturer_id))

        # Raise on bad status codes
        resp.raise_on_status()

        # If there are results, return them
        return resp.wrap_results(Manufacturer)[0]

    def create_manufacturer(self, name, slug):
        resp = self._request(
            method='post',
            url=self._format_url('/dcim/manufacturers'),
            json={
                'name': name,
                'slug': slug,
            })

        # Raise on bad status codes
        resp.raise_on_status()

        # Return the ID of the new interface
        return resp.results[0]['id']

    def delete_manufacturer(self, manufacturer_id):
        resp = self._request(
            method='delete',
            url=self._format_url('/dcim/manufacturers/{}', manufacturer_id))

        # Raise on bad status codes
        resp.raise_on_status()

    def device_type(self, device_type_id):
        resp = self._request(
            method='get',
            url=self._format_url('/dcim/device-types/{}', device_type_id))

        # Raise on bad status codes
        resp.raise_on_status()

        # If there are results, return them
        return resp.wrap_results(DeviceType)[0]

    def create_device_type(self, model, slug, u_height, manufacturer_id, part_number=None,
                           interface_ordering=InterfaceOrderConstant.BY_RACK_POSITION, is_console_server=False,
                           is_network_device=False, subdevice_role=SubdeviceTypeConstant.NONE, is_full_depth=False,
                           is_pdu=False, comments='', custom_fields=None):
        # Map constants
        if isinstance(subdevice_role, SubdeviceTypeConstant):
            subdevice_role = subdevice_role.value
        if isinstance(interface_ordering, InterfaceOrderConstant):
            interface_ordering = interface_ordering.value

        resp = self._request(
            method='post',
            url=self._format_url('/dcim/device-types'),
            json={
                'model': model,
                'slug': slug,
                'u_height': u_height,
                'is_pdu': is_pdu,
                'is_full_depth': is_full_depth,
                'subdevice_role': subdevice_role,
                'is_console_server': is_console_server,
                'is_network_device': is_network_device,
                'part_number': part_number,
                'interface_ordering': interface_ordering,
                'manufacturer': manufacturer_id,
                'comments': comments,
                'custom_fields': custom_fields if custom_fields is not None else dict()
            })

        # Raise on bad status codes
        resp.raise_on_status()

        # Return the ID of the new interface
        return resp.results[0]['id']

    def delete_device_type(self, device_type_id):
        resp = self._request(
            method='delete',
            url=self._format_url('/dcim/device-types/{}', device_type_id))

        # Raise on bad status codes
        resp.raise_on_status()

    def device_role(self, device_role_id):
        resp = self._request(
            method='get',
            url=self._format_url('/dcim/device-roles/{}', device_role_id))

        # Raise on bad status codes
        resp.raise_on_status()

        # If there are results, return them
        return resp.wrap_results(DeviceRole)[0]

    def create_device_role(self, name, slug, color='000000'):
        resp = self._request(
            method='post',
            url=self._format_url('/dcim/device-roles'),
            json={
                'name': name,
                'slug': slug,
                'color': color
            })

        # Raise on bad status codes
        resp.raise_on_status()

        # Return the ID of the new interface
        return resp.results[0]['id']

    def delete_device_role(self, device_role_id):
        resp = self._request(
            method='delete',
            url=self._format_url('/dcim/device-roles/{}', device_role_id))

        # Raise on bad status codes
        resp.raise_on_status()

    def device(self, device_id):
        """
        Get a device by the device's ID.

        :param device_id:
        :return:
        """
        resp = self._request(
            method='get',
            url=self._format_url('/dcim/devices/{}', device_id))

        # Raise on bad status codes
        resp.raise_on_status()

        # If there are results, return them
        return resp.wrap_results(Device)[0]

    def list_devices(self, **query):
        return self._list(Device, '/dcim/devices', query)

    def create_device(self, name, device_role_id, site_id, status=DeviceStatusConstant.ACTIVE, custom_fields=None,
                      comments='', rack_face=RackFaceConstant.FRONT, asset_tag=None, platform_id=None,
                      primary_ip4_id=None, primary_ip6_id=None, position=0, device_type_id=None, serial=None,
                      rack_id=None, tenant_id=None):
        # Map constants
        if isinstance(status, DeviceStatusConstant):
            status = status.value
        if isinstance(rack_face, RackFaceConstant):
            rack_face = rack_face.value

        resp = self._request(
            method='post',
            url=self._format_url('/dcim/devices'),
            json={
                'status': status,
                'device_role': device_role_id,
                'name': name,
                'site': site_id,
                'comments': comments,
                'face': rack_face,
                'asset_tag': asset_tag,
                'platform': platform_id,
                'device_type': device_type_id,
                'primary_ip4': primary_ip4_id,
                'primary_ip6': primary_ip6_id,
                'position': position,
                'serial': serial,
                'rack': rack_id,
                'tenant': tenant_id,
                'custom_fields': custom_fields if custom_fields is not None else dict()
            })

        # Raise on bad status codes
        resp.raise_on_status()

        # Return the ID of the new interface
        return resp.results[0]['id']

    def update_device(self, device_id, **fields):
        resp = self._request(
            method='patch',
            url=self._format_url('/dcim/devices/{}', device_id),
            json=fields)

        # Raise on bad status codes
        resp.raise_on_status()

    def delete_device(self, device_id):
        resp = self._request(
            method='delete',
            url=self._format_url('/dcim/devices/{}', device_id))

        # Raise on bad status codes
        resp.raise_on_status()


class IPAMClient(NetboxClientPart):
    def vrf(self, vrf_id):
        resp = self._request(
            method='get',
            url=self._format_url('/ipam/vrfs/{}', vrf_id))

        # Raise on bad status codes
        resp.raise_on_status()

        # If there are results, return them
        return resp.wrap_results(VRF)[0]

    def list_vrfs(self, **query):
        return self._list(VRF, '/ipam/vrfs', query)

    def create_vrf(self, name, route_distinguisher, tenant_id, enforce_unique=False, description=None,
                   custom_fields=None):
        """
        :return:
        """
        resp = self._request(
            method='post',
            url=self._format_url('/ipam/vrfs'),
            json={
                'name': name,
                'rd': route_distinguisher,
                'tenant': tenant_id,
                'enforce_unique': enforce_unique,
                'description': description,
                'custom_fields': custom_fields if custom_fields is not None else dict(),
            })

        # Raise on bad status codes
        resp.raise_on_status()

        # Return the ID of the new interface
        return resp.results[0]['id']

    def delete_vrf(self, vrf_id):
        resp = self._request(
            method='delete',
            url=self._format_url('/ipam/vrfs/{}', vrf_id))

        # Raise on bad status codes
        resp.raise_on_status()

    def prefix_role(self, prefix_role_id):
        resp = self._request(
            method='get',
            url=self._format_url('/ipam/roles/{}', prefix_role_id))

        # Raise on bad status codes
        resp.raise_on_status()

        # If there are results, return them
        return resp.wrap_results(PrefixRole)[0]

    def list_prefix_roles(self, **query):
        return self._list(PrefixRole, '/ipam/roles', query)

    def create_prefix_role(self, name, slug, weight=0):
        """
        :param name:
        :param slug:
        :param weight:
        :return:
        """
        resp = self._request(
            method='post',
            url=self._format_url('/ipam/roles'),
            json={
                'name': name,
                'slug': slug,
                'weight': weight
            })

        # Raise on bad status codes
        resp.raise_on_status()

        # Return the ID of the new interface
        return resp.results[0]['id']

    def delete_prefix_role(self, ipam_role_id):
        resp = self._request(
            method='delete',
            url=self._format_url('/ipam/roles/{}', ipam_role_id))

        # Raise on bad status codes
        resp.raise_on_status()

    def ip_address(self, ip_address_id):
        resp = self._request(
            method='get',
            url=self._format_url('/ipam/ip-addresses/{}', ip_address_id))

        # Raise on bad status codes
        resp.raise_on_status()

        # If there are results, return them
        return resp.wrap_results(IPAddress)[0]

    def list_ip_addresses(self, **query):
        return self._list(IPAddress, '/ipam/ip-addresses', query)

    def create_ip_address(self, address, status, tenant_id, role=None, interface_id=None, vrf_id=None,
                          nat_inside=None, description=None, custom_fields=None):
        # Map constants
        if isinstance(status, IPAddressStatusConstant):
            status = status.value
        if isinstance(role, IPAddressRoleConstant):
            role = role.value

        resp = self._request(
            method='post',
            url=self._format_url('/ipam/ip-addresses'),
            json={
                'description': description,
                'tenant': tenant_id,
                'interface': interface_id,
                'vrf': vrf_id,
                'role': role,
                'status': status,
                'address': address,
                'nat_inside': nat_inside,
                'custom_fields': custom_fields if custom_fields is not None else dict()
            })

        # Raise on bad status codes
        resp.raise_on_status()

        # Return the ID of the new interface
        return resp.results[0]['id']

    def delete_ip_address(self, ip_address_id):
        resp = self._request(
            method='delete',
            url=self._format_url('/ipam/ip-addresses/{}', ip_address_id))

        # Raise on bad status codes
        resp.raise_on_status()

    def assign_ip(self, address, interface_id, tenant_id, is_primary=False):
        """
        Assign an IP address to an interface.

        :param address:
        :param interface_id:
        :param tenant_id:
        :param is_primary:
        :return:
        """
        resp = self._request(
            method='post',
            url=self._format_url('/ipam/ip-addresses'),
            json={
                'is_primary': is_primary,
                'address': address,
                'interface': interface_id,
                'tenant': tenant_id
            })

        # Raise on bad status codes
        resp.raise_on_status()


class TenancyClient(NetboxClientPart):
    def tenant_group(self, tenant_group_id):
        resp = self._request(
            method='get',
            url=self._format_url('/tenancy/tenant-groups/{}', tenant_group_id))

        # Raise on bad status codes
        resp.raise_on_status()

        # If there are results, return them
        return resp.wrap_results(TenantGroup)[0]

    def list_tenant_groups(self, **query):
        return self._list(TenantGroup, '/tenancy/tenant-groups', query)

    def create_tenant_group(self, name, slug):
        resp = self._request(
            method='post',
            url=self._format_url('/tenancy/tenant-groups'),
            json={
                'name': name,
                'slug': slug
            })

        # Raise on bad status codes
        resp.raise_on_status()

        # Return the ID of the new interface
        return resp.results[0]['id']

    def delete_tenant_group(self, tenant_group_id):
        resp = self._request(
            method='delete',
            url=self._format_url('/tenancy/tenant-groups/{}', tenant_group_id))

        # Raise on bad status codes
        resp.raise_on_status()

    def tenant(self, tenant_id):
        """
        Get a tenant by the tenant's ID.

        :param tenant_id:
        :return:
        """
        resp = self._request(
            method='get',
            url=self._format_url('/tenancy/tenants/{}', tenant_id))

        # Raise on bad status codes
        resp.raise_on_status()

        # If there are results, return them
        return resp.wrap_results(Tenant)[0]

    def list_tenants(self, **query):
        return self._list(Tenant, '/tenancy/tenants', query)

    def create_tenant(self, name, slug, tenant_group_id, description=None, comments=None, custom_fields=None):
        resp = self._request(
            method='post',
            url=self._format_url('/tenancy/tenants'),
            json={
                'name': name,
                'slug': slug,
                'group': tenant_group_id,
                'description': description,
                'comments': comments,
                'custom_fields': custom_fields if custom_fields is not None else dict()
            })

        # Raise on bad status codes
        resp.raise_on_status()

        # Return the ID of the new interface
        return resp.results[0]['id']

    def delete_tenant(self, tenant_id):
        resp = self._request(
            method='delete',
            url=self._format_url('/tenancy/tenants/{}', tenant_id))

        # Raise on bad status codes
        resp.raise_on_status()
