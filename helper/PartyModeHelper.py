import json

from helper.Constants import Constants
from helper.SettingsSyncHelper import SettingsSyncHelper

settings_sync_helper = SettingsSyncHelper()


class PartyModeHelper:
    SETTING = "party-mode.json"
    SETTINGS_PATH = f"{Constants.settings_path()}/{SETTING}"

    def is_party_mode(self) -> bool:
        settings = self.get_settings()
        return settings["isPartyMode"]

    def enable_party_mode(self):
        settings = self.get_settings()
        settings["isPartyMode"] = True

        with open(PartyModeHelper.SETTINGS_PATH, "r+") as file:
            file.seek(0)
            json.dump(settings, file, indent=4)
            file.truncate()

    def disable_party_mode(self):
        settings = self.get_settings()
        settings["isPartyMode"] = False

        with open(PartyModeHelper.SETTINGS_PATH, "r+") as file:
            file.seek(0)
            json.dump(settings, file, indent=4)
            file.truncate()

    def toggle_party_mode(self):
        if self.is_party_mode():
            self.disable_party_mode()
        else:
            self.enable_party_mode()

    def get_settings(self):
        def _get_data():
            with open(self.SETTINGS_PATH) as file:
                data = json.load(file)
                return data

        try:
            return _get_data()
        except Exception:
            settings_sync_helper.reset_settings_file(self.SETTING)
            return _get_data()
