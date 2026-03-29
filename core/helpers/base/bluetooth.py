class BaseBluetoothHelper:
    def on_startup(self):
        raise NotImplementedError

    def is_discovery_on(self):
        raise NotImplementedError

    def toggle_bluetooth_discovery(self):
        raise NotImplementedError

    def turn_on(self):
        raise NotImplementedError

    def turn_off(self):
        raise NotImplementedError

    def is_bluetooth_on(self):
        raise NotImplementedError

    def bluetooth_discovery_on(self):
        raise NotImplementedError

    def bluetooth_discovery_off(self):
        raise NotImplementedError

    def get_bluetooth_display_name(self) -> str:
        raise NotImplementedError

    def change_bluetooth_display_name(self, name):
        raise NotImplementedError

    def connect(self, mac_address):
        raise NotImplementedError

    def disconnect(self, address=None):
        raise NotImplementedError

    def get_paired_devices(self) -> list:
        raise NotImplementedError

    def remove_device(self, address):
        raise NotImplementedError

    def get_connected_device(self):
        raise NotImplementedError

    def get_connected_device_name(self):
        raise NotImplementedError

    def is_connected(self):
        raise NotImplementedError

    def get_connected_device_mac(self):
        raise NotImplementedError
