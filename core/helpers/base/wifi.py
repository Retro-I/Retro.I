class BaseWifiHelper:
    def is_enabled(self):
        raise NotImplementedError

    def toggle_wifi(self):
        raise NotImplementedError

    def enable_wifi(self):
        raise NotImplementedError

    def disable_wifi(self):
        raise NotImplementedError

    def is_connected(self):
        raise NotImplementedError

    def get_networks(self):
        raise NotImplementedError

    def connect_to_wifi(self, ssid, password):
        raise NotImplementedError
