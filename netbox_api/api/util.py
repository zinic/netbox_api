from netbox_api.api.client import NetboxClient
from netbox_api.config import load_config


def new_api_client():
    cfg = load_config()
    ca_cert_path = cfg.get('netbox', 'ca_cert', default=None)

    # Create the API client
    return NetboxClient(
        cfg.get('netbox', 'host'),
        cfg.get('netbox', 'token'),
        verify=ca_cert_path)
