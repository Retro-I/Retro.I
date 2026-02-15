from core.helpers.base.settings_sync import BaseSettingsSyncHelper
from helper.SettingsSyncHelper import SettingsSyncHelper


class PiSettingsSyncHelper(BaseSettingsSyncHelper):
    def __init__(self):
        self.helper = SettingsSyncHelper()

    def validate_effects(self):
        self.helper.validate_effects()

    def validate_all_settings(self):
        self.helper.validate_all_settings()

    def reset_settings_file(self, filename):
        self.helper.reset_settings_file(filename)
