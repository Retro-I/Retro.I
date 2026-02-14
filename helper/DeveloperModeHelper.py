import json

from helper.Constants import Constants
from helper.SettingsSyncHelper import SettingsSyncHelper

c = Constants()
settings_sync_helper = SettingsSyncHelper()


class DeveloperModeHelper:
    SETTING = "developer-mode-settings.json"
    SETTINGS_PATH = f"{Constants.settings_path()}/{SETTING}"

    @staticmethod
    def is_developer_mode_active() -> bool:
        settings = DeveloperModeHelper.get_settings()
        return settings["isDeveloperModeActive"]

    @staticmethod
    def toggle_developer_mode_active(event):
        data = DeveloperModeHelper.get_settings()
        data["isDeveloperModeActive"] = event.control.value

        with open(DeveloperModeHelper.SETTINGS_PATH, "r+") as file:
            file.seek(0)
            json.dump(data, file, indent=4)
            file.truncate()

    @staticmethod
    def get_settings():
        def _get_data():
            with open(DeveloperModeHelper.SETTINGS_PATH) as file:
                data = json.load(file)
                return data

        try:
            return _get_data()
        except Exception:
            settings_sync_helper.reset_settings_file(
                DeveloperModeHelper.SETTING
            )
            return _get_data()
