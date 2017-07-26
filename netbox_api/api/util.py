from netbox_api.api.client import NetboxClient
from netbox_api.config import load_config


def new_api_client(host=None, port=80, scheme='http', token=None, ca_cert_path=None):
    if host is None and token is None:
        # If nothing was passed to us try to load the configuration as a last ditch
        cfg = load_config()

        host = cfg.get('netbox', 'host')
        port = cfg.get('netbox', 'port')
        token = cfg.get('netbox', 'token')
        scheme = cfg.get('netbox', 'scheme', default='http')
        ca_cert_path = cfg.get('netbox', 'ca_cert', default=None)

    # Create the API client
    return NetboxClient(
        host=host,
        port=port,
        scheme=scheme,
        token=token,
        verify=ca_cert_path)
