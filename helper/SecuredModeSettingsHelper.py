import json

from helper.Constants import Constants
from helper.SettingsSyncHelper import SettingsSyncHelper

c = Constants()
settings_sync_helper = SettingsSyncHelper()


class SecuredModeSettingsHelper:
    SETTING = "secured-mode-settings.json"
    SECURED_MODE_PATH = f"{c.settings_path()}/{SETTING}"

    def get_settings(self):
        def _get_data():
            with open(self.SECURED_MODE_PATH) as file:
                data = json.load(file)
                return data

        try:
            return _get_data()
        except Exception:
            settings_sync_helper.repair_settings_file(self.SETTING)
            return _get_data()

    def is_secured_mode_enabled(self) -> bool:
        data = self.get_settings()
        return data["securedModeEnabled"]
