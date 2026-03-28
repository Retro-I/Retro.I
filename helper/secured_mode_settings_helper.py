import json

from core.helpers.factories.settings_sync import create_settings_sync_helper
from helper.Constants import Constants

c = Constants()


class SecuredModeSettingsHelper:
    SETTING = "secured-mode-settings.json"
    SECURED_MODE_PATH = f"{Constants.settings_path()}/{SETTING}"

    def __init__(self):
        self.settings_sync_helper = create_settings_sync_helper()

    def get_settings(self):
        def _get_data():
            with open(self.SECURED_MODE_PATH) as file:
                data = json.load(file)
                return data

        try:
            return _get_data()
        except Exception:
            self.settings_sync_helper.reset_settings_file(self.SETTING)
            return _get_data()

    def is_secured_mode_enabled(self) -> bool:
        data = self.get_settings()
        return data["securedModeEnabled"]
