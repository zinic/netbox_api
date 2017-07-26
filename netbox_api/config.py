import os
import configparser


class ConfigException(Exception):
    def __init__(self, msg):
        super()
        self.msg = msg

    def __str__(self):
        return self.msg


class PynetboxConfig(object):
    def __init__(self, cfg_file):
        self._config = configparser.ConfigParser()
        self._config.read(cfg_file)

    def has_section(self, section):
        return section in self._config.sections()

    def has_options(self, section, *required_options):
        section_options = self._config.options(section)
        for option in required_options:
            if option not in section_options:
                return False
        return True

    def get(self, section, option, default=None):
        return self._config.get(section, option, fallback=default)


def config_path():
    # Make sure the config file exists
    cfg_file = os.path.expanduser('~/.netbox_api')
    if not os.path.exists(cfg_file):
        raise ConfigException('Configuration is missing. Please see the README for further instruction.')

    return cfg_file


def load_config():
    # Read our config
    cfg = PynetboxConfig(config_path())

    # Check that the config has what we need
    if not cfg.has_section('netbox') or not cfg.has_options('netbox', 'port', 'host', 'token'):
        raise ConfigException('Configuration is missing fields. Please see the README for further instruction.')

    return cfg
