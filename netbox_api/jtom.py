"""
JSON to Python Class object mapping package. This is a pile but it certainly gets the job done.
"""
import requests

CLS_DECLARATION_FMT = """
class {cls_name}(object):
    def __init__(self, {arg_list}):{arg_initializers}
    @classmethod
    def from_dict(cls, contents):
        if contents is None:
            return cls()
{arg_mappings}
        return cls(**contents)
"""

ARG_MAPPING_FMT = """
{indent}contents['{key}'] = contents['{raw_key}']
{indent}del contents['{raw_key}']
"""

ARG_LIST_FMT = """{prefix}{key}=None"""


class JSONObjectMapper():
    """
    JSON to Python Class object mapper
    """

    def __init__(self):
        pass

    @classmethod
    def _should_sanitize_key(cls, key):
        if key[0] == key[0].upper():
            return True

    @classmethod
    def _format(cls, fmt, **kwargs):
        return fmt.lstrip().format(**kwargs)

    @classmethod
    def _sanitize_key(cls, key):
        return key.lower()

    @classmethod
    def _indent_depth(cls, depth):
        # 4 Spaces per tab please
        num_spaces = depth * 4
        return ' ' * num_spaces

    @classmethod
    def _name_as_cls(cls, name):
        return ''.join([p[0].upper() + p[1:] for p in name.split('_')])

    def write_definitions(self, cls_name, source, path):
        definitions = self.handle_dict(cls_name, source)

        with open(path, 'w') as fout:
            fout.write('\n\n'.join(definitions))

    def handle_dict(self, cls_name, source):
        # Classes
        cls_list = list()

        # Initializer argument list
        arg_list = ''
        arg_initializers = '\n'
        arg_mappings = ''

        # Scan the keys to lay out our mapping strategy
        simple_objects = list()
        complex_objects = list()
        name_mappings = dict()

        for key, value in source.items():
            if self._should_sanitize_key(key):
                name_mappings[key] = self._sanitize_key(key)

            if isinstance(value, dict):
                complex_objects.append(key)
                cls_list.extend(self.handle_dict(self._name_as_cls(key), value))

            elif isinstance(value, list):
                raise NotImplementedError('List for key {}'.format(key))

            else:
                simple_objects.append(key)

        # Indent two levels in
        indent = self._indent_depth(2)

        # Iterate complex objects first
        for raw_key in complex_objects:
            key = self._sanitize_key(raw_key)

            arg_list += self._format(
                ARG_LIST_FMT,
                prefix=', ' if len(arg_list) > 0 else '',
                key=key)
            arg_initializers += '{indent}self.{key} = {key_cls}.from_dict({key})\n'.format(
                indent=indent,
                key=key,
                key_cls=self._name_as_cls(key))

        # Iterate simple objects next
        for raw_key in simple_objects:
            key = self._sanitize_key(raw_key)

            arg_list += self._format(
                ARG_LIST_FMT,
                prefix=', ' if len(arg_list) > 0 else '',
                key=key)
            arg_initializers += '{indent}self.{key} = {key}\n'.format(
                indent=indent,
                key=key)

        # Perform any argument mapping
        if len(name_mappings) > 0:
            arg_mappings = '\n'
            for raw_key, key in name_mappings.items():
                arg_mappings += self._format(
                    ARG_MAPPING_FMT,
                    indent=indent,
                    raw_key=raw_key,
                    key=key)

        # Append this class to the list and then return the list
        cls_list.append(
            self._format(CLS_DECLARATION_FMT,
                         cls_name=cls_name,
                         arg_list=arg_list,
                         arg_initializers=arg_initializers,
                         arg_mappings=arg_mappings))

        return cls_list


def map_api_objects():
    resp = requests.get(
        url='https://<host>/api/tenancy/tenants/1/',
        headers={
            'Authorization': 'Token <token>'
        },
        verify='<verify-path>')

    JSONObjectMapper().write_definitions('Tenant', resp.json(), './tenant.py')

    resp = requests.get(
        url='https://<host>/api/dcim/device/1/',
        headers={
            'Authorization': 'Token <token>'
        },
        verify='<verify-path>')

    JSONObjectMapper().write_definitions('Device', resp.json(), './devices.py')

    resp = requests.get(
        url='https://<host>/api/dcim/interfaces/1/',
        headers={
            'Authorization': 'Token <token>'
        },
        verify='<verify-path>')

    JSONObjectMapper().write_definitions('Interface', resp.json(), './interfaces.py')

    resp = requests.get(
        url='https://<host>/api/dcim/sites/2/',
        headers={
            'Authorization': 'Token <token>'
        },
        verify='<verify-path>')

    JSONObjectMapper().write_definitions('Site', resp.json(), './sites.py')


if __name__ == '__main__':
    map_api_objects()
