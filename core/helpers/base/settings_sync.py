class BaseSettingsSyncHelper:
    def validate_effects(self):
        raise NotImplementedError

    def validate_all_settings(self):
        raise NotImplementedError

    def reset_settings_file(self, filename):
        raise NotImplementedError
