class BaseSecuredModeSettings:
    def get_settings(self):
        raise NotImplementedError

    def is_secured_mode_enabled(self) -> bool:
        raise NotImplementedError
