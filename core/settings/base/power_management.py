class BasePowerManagementSettings:
    def is_enabled(self) -> bool:
        raise NotImplementedError

    def get_management_settings(self):
        raise NotImplementedError

    def shutdown_time_reached(self) -> bool:
        raise NotImplementedError
