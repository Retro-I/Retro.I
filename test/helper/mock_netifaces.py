import netifaces


def mock_wifi_netifaces(mock_gateways, mock_ifaddresses):
    mock_gateways.return_value = {
        "default": {
            netifaces.AF_INET: ("192.168.2.1", "wlan0"),
            netifaces.AF_INET6: ("fe80::b6a5:efff:fedb:b5e0", "wlan0"),
        },
        netifaces.AF_INET: [
            ("192.168.2.1", "wlan0", True),
        ],
        netifaces.AF_INET6: [
            ("fe80::b6a5:efff:fedb:b5e0", "wlan0", True),
        ],
    }

    mock_ifaddresses.return_value = {
        netifaces.AF_LINK: [
            {"addr": "XX:XX:XX:XX:XX:XX"},
        ],
        netifaces.AF_INET: [
            {
                "addr": "192.168.2.106",
                "netmask": "255.255.255.0",
            },
        ],
        netifaces.AF_INET6: [
            {
                "addr": "fd9e:f19c:c4eb:1:4641:396c:3ff3:f24b",
                "netmask": "ffff:ffff:ffff:ffff::/64",
            },
        ],
    }


def mock_lan_netifaces(mock_gateways, mock_ifaddresses):
    mock_gateways.return_value = {
        "default": {
            netifaces.AF_INET: ("192.168.2.1", "eth0"),
            netifaces.AF_INET6: ("fe80::b6a5:efff:fedb:b5e0", "wlan0"),
        },
        netifaces.AF_INET: [
            ("192.168.2.1", "eth0", True),
        ],
        netifaces.AF_INET6: [
            ("fe80::b6a5:efff:fedb:b5e0", "wlan0", True),
        ],
    }

    mock_ifaddresses.return_value = {
        netifaces.AF_LINK: [
            {"addr": "AB:DE:EF:GH:IJ:KL"},
        ],
        netifaces.AF_INET: [
            {
                "addr": "192.168.2.100",
                "netmask": "255.255.0.0",
            },
        ],
        netifaces.AF_INET6: [
            {
                "addr": "fd9e:f19c:c4eb:1:4641:396c:3ff3:f24b",
                "netmask": "ffff:ffff:ffff:ffff::/64",
            },
        ],
    }


def mock_none_netifaces(mock_gateways, mock_ifaddresses):
    mock_gateways.return_value = {"default": {}}
    mock_ifaddresses.return_value = {}
