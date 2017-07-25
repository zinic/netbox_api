import json

import requests
import requests.auth

from netbox_api.model import Device, Site, Tenant, Interface


class NetboxTokenAuth(requests.auth.AuthBase):
    """
    Attaches Netbox-style HTTP Token Authentication to the given Request object.
    """

    def __init__(self, token):
        self.token = token

    def __eq__(self, other):
        return all([
            self.token == getattr(other, 'token', None),
        ])

    def __ne__(self, other):
        return not self == other

    def __call__(self, r):
        r.headers['Authorization'] = 'Token {}'.format(self.token)
        return r


class ClientException(Exception):
    def __init__(self, msg, failures=None):
        self.msg = msg
        self.failures = failures


class NetboxResponse(object):
    def __init__(self, resp, content):
        self._response = resp
        self._content = content
        self._json = None

    def _parse_content(self):
        payload = json.loads(self._content)

        # Single entity requests don't have the result wrapper JSON so we
        # choose to emulate it - DRY
        if 'results' not in payload:
            return {
                'count': 1,
                'next': None,
                'previous': None,
                'results': [payload]
            }

        return payload

    def raise_on_status(self):
        if self.ok is False:
            raise ClientException('Unexpected status code: {}\n{}'.format(
                self._response.status_code,
                self._content))

    def wrap_results(self, cls):
        return [cls(**v) for v in self.results]

    @property
    def json(self):
        if self._json is None:
            self._json = self._parse_content()

        return self._json

    @property
    def status_code(self):
        return self._response.status_code

    @property
    def ok(self):
        return 200 <= self._response.status_code < 300

    @property
    def count(self):
        return self.json['count']

    @property
    def next_page(self):
        return self.json['next']

    @property
    def previous_page(self):
        return self.json['previous']

    @property
    def results(self):
        return self.json['results']


def _overwrite_header(header_name, new_value, headers):
    target = header_name
    for key, value in headers.items():
        if key.lower() == header_name.lower():
            target = key
            break

    headers[target] = new_value


class NetboxClient(object):
    def __init__(self, host, token, scheme='https', verify=None):
        self._host = host
        self._scheme = scheme
        self._auth = NetboxTokenAuth(token)
        self._verify_path = verify

    def _request(self, method, url, **kwargs):
        request_func = getattr(requests, method)

        # Copy the kwargs dict to modify it
        request_kwargs = kwargs.copy()
        request_kwargs['auth'] = self._auth

        if self._verify_path is not None:
            request_kwargs['verify'] = self._verify_path

        # Overwrite Accept header
        if 'headers' in request_kwargs:
            _overwrite_header('Accept', 'application/json', request_kwargs['headers'])

        # Make the request
        resp = request_func(
            url=url,
            **request_kwargs)

        try:
            # Wrap the request which should read the entire body
            return NetboxResponse(resp, resp.text)
        finally:
            # Eagerly close the response
            resp.close()

    def _paginate_requests(self, cls, method, url, **kwargs):
        resp = self._request(method, url=url, **kwargs)

        while True:
            # Raise on bad status
            resp.raise_on_status()

            # Yield the next page of results
            for r in resp.wrap_results(cls):
                yield r

            # Exit this loop if there isn't a next page
            if resp.next_page is None:
                break

            # Perform the next get
            resp = self._request('get', url=resp.next_page)

    def _format_url(self, path_fmt, *parts):
        # Strip leading slashes
        if path_fmt.startswith('/'):
            path_fmt = path_fmt[1:]

        # Strip trailing slashes
        if path_fmt.endswith('/'):
            path_fmt = path_fmt[:len(path_fmt) - 1]

        # Format the path
        path = path_fmt.format(*parts)

        return '{}://{}/api/{}/'.format(
            self._scheme,
            self._host,
            path)

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
        return resp.wrap_results(Interface)

    def lookup_device_interface(self, device_name, interface_name):
        """
        Look up a device interface by the device name and interface name.

        :param device_name:
        :param interface_name:
        :return:
        """
        resp = self._request(
            method='get',
            url=self._format_url('/dcim/interfaces'),
            params={
                'name': interface_name,
                'device': device_name
            })

        # Raise on bad status codes
        resp.raise_on_status()

        # If there are results, return them
        return resp.wrap_results(Interface)

    def lookup_device_interfaces(self, device_name):
        """
        Look up all device interfaces by device name.

        :param device_name:
        :return:
        """
        resp = self._request(
            method='get',
            url=self._format_url('/dcim/interfaces'),
            params={
                'device': device_name
            })

        # Raise on bad status codes
        resp.raise_on_status()

        # If there are results, return them
        return resp.wrap_results(Interface)

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
        return resp.wrap_results(Tenant)

    def lookup_tenant(self, tenant_name):
        """
        Look up a tenant by the tenant's name.

        :param tenant_name:
        :return:
        """
        resp = self._request(
            method='get',
            url=self._format_url('/tenancy/tenants'),
            params={'name': tenant_name})

        # Raise on bad status codes
        resp.raise_on_status()

        # If there are results, return them
        return resp.wrap_results(Tenant)

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
        return resp.wrap_results(Site)

    def lookup_site(self, site_name):
        """
        Lookup a site by the site's name.

        :param site_name:
        :return:
        """
        resp = self._request(
            method='get',
            url=self._format_url('/dcim/sites'),
            params={'name': site_name})

        # Raise on bad status codes
        resp.raise_on_status()

        # If there are results, return them
        return resp.wrap_results(Site)

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
        return resp.wrap_results(Device)

    def lookup_device(self, device_name):
        """
        Look up a device by the device's name.

        :param device_name:
        :return:
        """
        resp = self._request(
            method='get',
            url=self._format_url('/dcim/devices'),
            params={'name': device_name})

        # Raise on bad status codes
        resp.raise_on_status()

        # If there are results, return them
        return resp.wrap_results(Device)

    def list_devices(self, **params):
        """
        List devices via a number of available search parameters specified as keyword arguments.

        :param params:
        :return:
        """
        result_iter = self._paginate_requests(
            cls=Device,
            method='get',
            url=self._format_url('/dcim/devices'),
            params=params)

        return [r for r in result_iter]

    def update_device_custom_fields(self, device_id, custom_fields):
        """
        Update a device's custom fields value with new custom fields.

        :param device_id:
        :param custom_fields:
        :return:
        """
        resp = self._request(
            method='patch',
            url=self._format_url('/dcim/devices/{}', device_id),
            json={
                'custom_fields': custom_fields
            })

        # Raise on bad status codes
        resp.raise_on_status()
