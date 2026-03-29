class BasePartyModeSettings:
    def is_party_mode(self) -> bool:
        raise NotImplementedError

    def enable_party_mode(self):
        raise NotImplementedError

    def disable_party_mode(self):
        raise NotImplementedError

    def toggle_party_mode(self):
        raise NotImplementedError

    def get_settings(self):
        raise NotImplementedError
