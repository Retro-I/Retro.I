import json

from core.helpers.factories.settings_sync import create_settings_sync_helper
from helper.Constants import Constants

c = Constants()


class StartupErrorHelper:
    SETTING = "startup-error.json"
    STARTUP_ERROR_PATH = f"{Constants.settings_path()}/{SETTING}"

    def __init__(self):
        self.settings_sync_helper = create_settings_sync_helper()

    def get_settings(self):
        def _get_data():
            with open(self.STARTUP_ERROR_PATH) as file:
                data = json.load(file)
                return data

        try:
            return _get_data()
        except Exception:
            self.settings_sync_helper.reset_settings_file(self.SETTING)
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
