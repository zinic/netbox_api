import sys

from tabulate import tabulate

from netbox_api.api import new_api_client
from netbox_api.sync import synchronize_host
from netbox_api.util import parse_args


def _lookup_device(client, device_name):
    matching_devices = client.dcim.list_devices(name=device_name)
    if len(matching_devices) == 0:
        raise Exception('Unable to find a device by name: {}'.format(device_name))

    return matching_devices[0]


def update_device_tags(client, device_name, tags):
    device = _lookup_device(client, device_name)

    # Tags are stored as a custom field
    client.dcim.update_device(device.id, custom_fields={
        'Tags': ','.join([t.strip() for t in tags])
    })

    # Show the device last to reflect the update
    show_device(client, device_name)


def show_device(client, device_name):
    device = _lookup_device(client, device_name)

    print('Name: {}'.format(device.name))
    print('Model: {}\n'.format(device.device_type.model))

    print('Custom Fields:')
    for k, v in device.custom_fields.items():
        print('  {}: {}'.format(k, v))


def _device_tags_match(device, tags):
    for other_tag in tags:
        if other_tag not in device.custom_fields['Tags']:
            return False

    return True


def list_devices(client, tags, verbose, show_iface):
    if verbose:
        list_devices_table(client, tags, show_iface)
    else:
        for device in client.dcim.list_devices(cf_Tags=tags[0]):
            if _device_tags_match(device, tags) is False:
                continue

            print(device.name)


def list_devices_table(client, tags, show_iface):
    table = list()

    for device in client.dcim.list_devices(cf_Tags=tags[0]):
        if _device_tags_match(device, tags) is False:
            continue

        mac_addr = ''
        device_interfaces = client.dcim.list_interfaces(device=device.name)

        if show_iface is not None:
            for interface in device_interfaces:
                if interface.name == show_iface:
                    mac_addr = interface.mac_address

        elif len(device_interfaces) > 0:
            mac_addr = device_interfaces[0].mac_address

        table.append([
            device.rack.display_name,
            device.position,
            device.name,
            device.device_type.model,
            mac_addr,
            device.custom_fields['Tags']])

    print(tabulate(table, headers=['Rack', 'Rack Position', 'Name', 'Device Model', 'MAC Addr', 'Tags']))


def main():
    # Make sure we let the user know that this is Python 3 only
    if sys.version_info < (3, 5):
        print('This utility is only supported on Python 3.5.x and forward.')
        return

    args = parse_args()
    client = new_api_client()

    if args.root_cmd == 'sync':
        synchronize_host(client)

    elif args.root_cmd == 'devices':
        if args.devices_cmd == 'list':
            list_devices(client, args.tags, args.verbose, args.show_iface)

        elif args.devices_cmd == 'show':
            show_device(client, args.device)

        elif args.devices_cmd == 'tags':
            if args.devices_tags_cmd == 'update':
                update_device_tags(client, args.device, args.tags)

    elif args.root_cmd == 'racks':
        if args.racks_cmd == 'show':
            units_available = list()

            for rack_unit in client.rack_units(args.rack):
                if rack_unit.device is None:
                    units_available.append(rack_unit)

            for available_unit in units_available:
                print(available_unit.id)


if __name__ == '__main__':
    main()
