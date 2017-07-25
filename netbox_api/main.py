import sys

from tabulate import tabulate

from netbox_api.api import new_api_client
from netbox_api.sync import synchronize_host
from netbox_api.util import parse_args


def _lookup_device(client, device_name):
    device_list = client.lookup_device(device_name)
    if len(device_list) == 0:
        raise Exception('Unable to find a device by name: {}'.format(device_name))

    return device_list[0]


def update_device_tags(client, device_name, tags):
    device = _lookup_device(client, device_name)
    client.update_device_custom_fields(device.id, {
        'Tags': ','.join([t.strip() for t in tags])
    })

    # Show the device last to reflect the update
    show_device(client, device_name)


def show_device(client, device_name):
    device = _lookup_device(client, device_name)

    print('Name: {}'.format(device.name))
    print('Model: {}'.format(device.device_type.model))
    print('')
    print('Tags: {}'.format(device.custom_fields.tags))


def list_devices(client, tags, verbose, show_iface):
    if verbose:
        list_devices_table(client, tags, show_iface)
    else:
        for device in client.list_devices(cf_Tags=tags[0]):
            print(device.name)


def list_devices_table(client, tags, show_iface):
    table = list()

    for device in client.list_devices(cf_Tags=tags[0]):
        mac_addr = ''
        device_interfaces = client.lookup_device_interfaces(device.name)

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
            device.custom_fields.tags])

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
