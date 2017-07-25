## netbox_api
[Netbox](https://github.com/digitalocean/netbox) Python CLI and API Client

## API Compatibility
* Netbox >= v2.0.10

## Installation

##### Python 3.x Only
`netbox_api` currently only supports Python 3.x and greater.

#### Installing from PyPI

```bash
# Install from PyPI
pip install netbox_api

# After this, your python install should have the runscript in its bin folder
netbox_api --help
```

## Uninstalling

Uninstalling netbox_api is easy!

```bash
pip uninstall -y netbox_api
```

## Updating

Updating netbox_api is easy, too!

```bash
pip install --upgrade netbox_api
```

## Configuration

netbox_api expects a configuration to inform it where Netbox is hosted and what
credentials to use when contacting its API.

#### Location

The netbox_api configuration is located at `~/.netbox_api` and is read as an INI file.

#### Example

```ini
[netbox]
host = netbox.example.com
username = user_api_token
ca_cert = /path/to_a_ca_cert/that_can_validate
```

## Library Usage

netbox_api is simple to initialize and begin using.

```python
import netbox_api

# Creating the client requires a valid config. See the configuration section of the README for this.
client = netbox_api.new_api_client()

# Lookup methods will always return a list since many devices may match a given name.
devices = client.lookup_device('device-name')
for device in devices:
    print(device.name)
```

## CLI Usage

netbox_api comes out of the box with a rich CLI that contains all the help information you may need.

```bash
# Top-level help is available
netbox_api --help

# Sub-commands also have contextual help output
netbox_api devices --help
```

#### Examples
##### Listing Devices with Tags

Tags are a custom field commonly used - the CLI has direct support for the idiom but its use is not required.

```bash
# Simple listing
netbox_api devices list -t unused

# Be verbose and output a device info table
netbox_api devices list -v -t unused
```

## License

This software is made available to you under the [MIT License](LICENSE).
