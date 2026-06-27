class BasePowerManagementSettings:
    def is_enabled(self) -> bool:
        raise NotImplementedError

    def get_management_settings(self):
        raise NotImplementedError
