import datetime
import json

from core.factories.helper_factories import create_settings_sync_helper
from core.settings.base.power_management import BasePowerManagementSettings
from helper.constants import Constants

c = Constants()


class PiPowerManagementSettings(BasePowerManagementSettings):
    SETTING = "power-management-settings.json"
    SETTINGS_PATH = f"{Constants.settings_path()}/{SETTING}"

    _last_shutdown_check = None

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

    def shutdown_time_reached(self) -> bool:
        now = datetime.datetime.now()
        settings = self.get_settings()

        if not settings["enabled"]:
            return False

        weekday = now.weekday()
        settings_today = next(
            (s for s in settings["items"] if s["id"] == weekday), None
        )

        if self._last_shutdown_check is None:
            self._last_shutdown_check = now
            return False

        result = False

        if settings_today["enabled"]:
            shutdown_time = datetime.datetime.strptime(
                settings_today["time"],
                "%H:%M",
            ).time()

            crossed_today = (
                self._last_shutdown_check.date() == now.date()
                and self._last_shutdown_check.time()
                <= shutdown_time
                <= now.time()
            )
            result = crossed_today

        self._last_shutdown_check = now

        return result
