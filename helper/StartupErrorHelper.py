import json

from helper.Constants import Constants
from helper.SettingsSyncHelper import SettingsSyncHelper

c = Constants()
settings_sync_helper = SettingsSyncHelper()


class StartupErrorHelper:
    SETTING = "startup-error.json"
    STARTUP_ERROR_PATH = f"{Constants.settings_path()}/{SETTING}"

    def get_settings(self):
        def _get_data():
            with open(self.STARTUP_ERROR_PATH) as file:
                data = json.load(file)
                return data

        try:
            return _get_data()
        except Exception:
            settings_sync_helper.repair_settings_file(self.SETTING)
            return _get_data()

    def is_startup_error(self):
        data = self.get_settings()
        return data["isStartupError"]

    def startup_error(self) -> str:
        data = self.get_settings()
        return data["startupErrorMessage"]

    def write_startup_error(self, message: str = ""):
        data = self.get_settings()
        data["isStartupError"] = True
        data["startupErrorMessage"] = message

        with open(self.STARTUP_ERROR_PATH, "r+") as file:
            file.seek(0)
            json.dump(data, file, indent=4)
            file.truncate()

    def reset_startup_error(self):
        data = self.get_settings()
        data["isStartupError"] = False
        data["startupErrorMessage"] = ""

        with open(self.STARTUP_ERROR_PATH, "r+") as file:
            file.seek(0)
            json.dump(data, file, indent=4)
            file.truncate()
