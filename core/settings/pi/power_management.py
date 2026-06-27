import json

from core.factories.helper_factories import create_settings_sync_helper
from core.settings.base.power_management import BasePowerManagementSettings
from helper.constants import Constants

c = Constants()


class PiPowerManagementSettings(BasePowerManagementSettings):
    SETTING = "power-management-settings.json"
    SETTINGS_PATH = f"{Constants.settings_path()}/{SETTING}"

    def __init__(self):
        self.settings_sync_helper = create_settings_sync_helper()

    def get_settings(self):
        def _get_data():
            with open(self.SETTINGS_PATH) as file:
                data = json.load(file)
                return data

        try:
            return _get_data()
        except Exception:
            self.settings_sync_helper.reset_settings_file(self.SETTING)
            return _get_data()

    def is_enabled(self) -> bool:
        return bool(self.get_settings()["enabled"])

    def get_management_settings(self) -> list:
        return self.get_settings()["items"]

    def enable_power_management(self):
        data = self.get_settings()
        data["enabled"] = True

        with open(self.SETTINGS_PATH, "r+") as file:
            file.seek(0)
            json.dump(data, file, indent=4)
            file.truncate()

    def disable_power_management(self):
        data = self.get_settings()
        data["enabled"] = False

        with open(self.SETTINGS_PATH, "r+") as file:
            file.seek(0)
            json.dump(data, file, indent=4)
            file.truncate()

    def update_management_settings(self, item: dict):
        data = self.get_settings()
        for i, day in enumerate(data["items"]):
            if day["id"] == item["id"]:
                data["items"][i]["time"] = item["time"]
                data["items"][i]["enabled"] = item["enabled"]
                break

        with open(self.SETTINGS_PATH, "r+") as file:
            file.seek(0)
            json.dump(data, file, indent=4)
            file.truncate()
