import json

from core.helpers.factories.settings_sync import create_settings_sync_helper
from helper.Constants import Constants

c = Constants()


class ScrollbarSettingsHelper:
    SETTING = "scrollbar-settings.json"
    SCROLLBAR_SETTINGS_PATH = f"{Constants.settings_path()}/{SETTING}"

    def __init__(self):
        self.settings_sync_helper = create_settings_sync_helper()

    def get_settings(self):
        def _get_data():
            with open(self.SCROLLBAR_SETTINGS_PATH) as file:
                data = json.load(file)
                return data

        try:
            return _get_data()
        except Exception:
            self.settings_sync_helper.reset_settings_file(self.SETTING)
            return _get_data()

    def is_scrollbar_enabled(self) -> bool:
        return bool(self.get_settings()["showScrollbar"])

    def toggle_scrollbar_enabled(self):
        data = self.get_settings()
        data["showScrollbar"] = not self.is_scrollbar_enabled()

        with open(self.SCROLLBAR_SETTINGS_PATH, "r+") as file:
            file.seek(0)
            json.dump(data, file, indent=4)
            file.truncate()
