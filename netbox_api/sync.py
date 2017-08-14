"""
Synchronize a local machine's details with information in NetBox via NetBox HTTP APIs.

TODO
====

  * Support passing of token credentials via an environment variable to make
    consumption of this automation easier.

Currently Supported Features
============================

  * Interface discovery and registration

"""

import re

from netbox_api.cmdutil import do_exec
from netbox_api.model import Interface, FormFactorConstant

# Regex for pulling out the IP address from the output of the CLI tool 'ip'
_IP_TOOL_RE = re.compile('inet\\s+([^\\s]+)')

# Regex for pulling out port type information from the output of ethtool
_ETHTOOL_PORT_RE = re.compile('[^:]+:\\s+\\[([^\\]]+)\\]')

# Dictionary of port types from what ethtool output to what netbox expects
_PORT_TYPES = {
    'tp': FormFactorConstant.BASE_T_1GE,
    'fibre': FormFactorConstant.SFP_PLUS_10GE
}


def _parse_interface_info(output):
    interfaces = list()

    # Interface info
    i = 0
    lines = output.splitlines()

    while i < len(lines):
        iface_name = lines[i]
        mac_address = lines[i + 1]
        i += 2

        # Create the new interface and add it to the list
        interface = Interface(name=iface_name)
        interface.mac_address = mac_address

        interfaces.append(interface)

    return interfaces


def _list_interfaces():
    result = do_exec('ls -1 /sys/class/net/')
    return result.stdout.splitlines()


def _iface_ip_addr(iface):
    result = do_exec('ip -4 addr show {}'.format(iface))

    match = _IP_TOOL_RE.search(result.stdout)
    if match is not None:
        return match.group(1)

    return None


def _iface_mac_addr(iface):
    with open('/sys/class/net/{}/address'.format(iface), 'r') as fin:
        return fin.read().strip()


def _ethtool_iface(iface):
    result = do_exec('ethtool {}'.format(iface))
    return result.stdout


def _iface_port_type(iface):
    iface_details = _ethtool_iface(iface)

    port_type = None
    for line in [l.strip() for l in iface_details.splitlines()]:
        if line.lower().startswith('supported ports:'):
            match = _ETHTOOL_PORT_RE.match(line)
            if match is None:
                raise Exception('Unable to match port type RE against: {}'.format(line))

            port_type = match.group(1).strip().lower()

    if port_type is not None:
        return _PORT_TYPES[port_type]

    return None


def _hostname():
    result = do_exec('hostname -f')
    return result.stdout


def synchronize_host(netbox_client):
    # Get the hostname
    hostname = _hostname()

    # The simple hostname (left most component) is the device name key
    simple_hostname = hostname if '.' not in hostname else hostname.split('.')[0]

    # Look up the device definition
    tenant = netbox_client.tenancy.list_tenants(name='Infrastructure')[0]
    device = netbox_client.dcim.list_devices(name=simple_hostname)[0]

    # Clear old interfaces if we can
    for interface in netbox_client.dcim.list_interfaces(device=simple_hostname):
        netbox_client.delete_interface(interface.id)

    # Iterate through the real HW devices
    for iface_name in _list_interfaces():
        # Ignore devices that don't matter to us
        if iface_name in ['lo'] or 'tun' in iface_name:
            continue

        # Gather information related to the interface in question
        ip_addr = _iface_ip_addr(iface_name)
        mac_addr = _iface_mac_addr(iface_name)
        form_factor = _iface_port_type(iface_name)

        # We can not continue without a form_factor so bail here if it's None
        if form_factor is None:
            raise Exception('Unable to determine port type for interface: {}'.format(iface_name))

        # Add this interface definition to the device
        iface_id = netbox_client.dcim.create_interface(iface_name, form_factor, device.id, mac_addr)

        # If there's an IP address, assign it to the device as well
        if ip_addr is not None:
            netbox_client.ipam.assign_ip(ip_addr, iface_id, tenant.id)
