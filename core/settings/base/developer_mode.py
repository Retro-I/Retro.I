class BaseDeveloperModeSettings:
    @staticmethod
    def is_developer_mode_active() -> bool:
        raise NotImplementedError

    @staticmethod
    def toggle_developer_mode_active(event):
        raise NotImplementedError

    @staticmethod
    def get_settings():
        raise NotImplementedError
