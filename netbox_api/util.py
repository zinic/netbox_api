import sys
import argparse


# Simple alias to save me some annoyance elsewhere
def halt(msg='', retcode=0):
    if msg is not None and msg != '':
        print(msg)

    sys.exit(retcode)


def _gen_argparser():
    # netbox
    root_cmd = argparse.ArgumentParser(description='Netbox API/DB Integrations and Tools CLI')
    root_cmds = root_cmd.add_subparsers(
        title='Available Commands',
        dest='root_cmd')
    root_cmds.required = True

    # netbox devices
    root_cmds.add_parser('sync', help='Synchronize infrastructure information for this machine.')

    # netbox devices
    devices_cmd = root_cmds.add_parser('devices', help='Manage and inspect devices.')
    devices_cmds = devices_cmd.add_subparsers(
        title='Available Commands',
        dest='devices_cmd')

    # netbox devices show
    devices_show_cmd = devices_cmds.add_parser('show', help='Show details for a single device.')
    devices_show_cmd.add_argument(
        '--verbose', '-v',
        action='store_true',
        default=False,
        dest='verbose',
        help='Emit more information.')

    devices_show_cmd.add_argument(
        dest='device',
        help='Name of the device to look up.')

    # netbox devices tags
    devices_tags_cmd = devices_cmds.add_parser('tags', help='Manage and inspect device tagging.')
    devices_tags_cmds = devices_tags_cmd.add_subparsers(
        title='Available Commands',
        dest='devices_tags_cmd')

    # netbox devices tags update
    devices_tags_update_cmd = devices_tags_cmds.add_parser('update', help='Manage and inspect devices.')
    devices_tags_update_cmd.add_argument(
        dest='device',
        help='Name of the device to edit.')

    devices_tags_update_cmd.add_argument(
        dest='tags',
        nargs='+',
        help='Name of the device to edit.')

    # netbox devices list
    devices_list_cmd = devices_cmds.add_parser('list', help='List devices.')
    devices_list_cmd.add_argument(
        '--verbose', '-v',
        action='store_true',
        default=False,
        dest='verbose',
        help='Emit more information.')

    devices_list_cmd.add_argument(
        '--tag', '-t',
        action='append',
        default=list(),
        dest='tags',
        help='Select devices with this tag. May be specified multiple times.')

    devices_list_cmd.add_argument(
        '--show-iface', '-i',
        dest='show_iface',
        help='Select an interface to output inline with the verbose table.')

    return root_cmd


def print_help():
    _gen_argparser().print_help()


def parse_args():
    root_cmd = _gen_argparser()
    if len(sys.argv) == 1:
        root_cmd.print_help()
        halt(retcode=1)

    args = root_cmd.parse_args()
    if args is None:
        halt(retcode=1)

    return args
