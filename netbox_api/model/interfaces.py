# Form factor constants
from enum import Enum


class FormFactorConstants(Enum):
    # Virtual interfaces
    VIRTUAL = 0
    LAG = 200

    # Ethernet (fixed)
    BASE_TX_10_100ME = 800
    BASE_T_1GE = 1000
    GBASE_T_10GE = 1150

    # Ethernet (modular)
    GBIC_1GE = 1050
    SFP_1GE = 1100
    SFP_PLUS_10GE = 1200
    XFP_10GE = 1300
    XENPAK_10GE = 1310
    X2_10GE = 1320
    SFP28_25GE = 1350
    QSFP_PLUS_40GE = 1400
    CFP_100GE = 1500
    QSFP28_100GE = 1600

    # FibreChannel
    SFP_1GFC = 3010
    SFP_2GFC = 3020
    SFP_4GFC = 3040
    SFP_PLUS_8GFC = 3080
    SFP_PLUS_16GFC = 3160

    # Serial
    T1 = 4000
    E1 = 4010
    T3 = 4040
    E3 = 4050

    # Stacking
    CISCO_STACK_WISE = 5000
    CISCO_STACK_WISE_PLUS = 5050
    CISCO_FLEX_STACK = 5100
    CISCO_FLEX_STACK_PLUS = 5150
    JUNIPER_VCP = 5200

    # Other
    OTHER = 32767


class FormFactor(object):
    def __init__(self, value=None, label=None):
        self.value = value
        self.label = label

    @classmethod
    def from_dict(cls, contents):
        if contents is None:
            return cls()

        return cls(**contents)


class Connection(object):
    def __init__(self, id=None, url=None, connection_status=None):
        self.id = id
        self.url = url
        self.connection_status = connection_status

    @classmethod
    def from_dict(cls, contents):
        if contents is None:
            return cls()

        return cls(**contents)


class InterfaceDevice(object):
    def __init__(self, id=None, url=None, name=None, display_name=None):
        self.id = id
        self.url = url
        self.name = name
        self.display_name = display_name

    @classmethod
    def from_dict(cls, contents):
        if contents is None:
            return cls()

        return cls(**contents)


class FormFactor(object):
    def __init__(self, value=None, label=None):
        self.value = value
        self.label = label

    @classmethod
    def from_dict(cls, contents):
        if contents is None:
            return cls()

        return cls(**contents)


class ConnectedInterface(object):
    def __init__(self, device=None, form_factor=None, id=None, url=None, name=None, lag=None, mac_address=None,
                 mgmt_only=None, description=None):
        self.device = InterfaceDevice.from_dict(device)
        self.form_factor = FormFactor.from_dict(form_factor)
        self.id = id
        self.url = url
        self.name = name
        self.lag = lag
        self.mac_address = mac_address
        self.mgmt_only = mgmt_only
        self.description = description

    @classmethod
    def from_dict(cls, contents):
        if contents is None:
            return cls()

        return cls(**contents)


class Interface(object):
    def __init__(self, device=None, form_factor=None, connection=None, connected_interface=None, id=None, name=None,
                 lag=None, mac_address=None, mgmt_only=None, description=None):
        self.device = InterfaceDevice.from_dict(device)
        self.form_factor = FormFactor.from_dict(form_factor)
        self.connection = Connection.from_dict(connection)
        self.connected_interface = ConnectedInterface.from_dict(connected_interface)
        self.id = id
        self.name = name
        self.lag = lag
        self.mac_address = mac_address
        self.mgmt_only = mgmt_only
        self.description = description

    @classmethod
    def from_dict(cls, contents):
        if contents is None:
            return cls()

        return cls(**contents)
