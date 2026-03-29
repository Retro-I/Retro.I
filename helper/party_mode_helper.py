import json

from helper.constants import Constants

from core.helpers.factories.settings_sync import create_settings_sync_helper


class PartyModeHelper:
    SETTING = "party-mode.json"
    SETTINGS_PATH = f"{Constants.settings_path()}/{SETTING}"

    def __init__(self):
        self.settings_sync_helper = create_settings_sync_helper()

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
            self.settings_sync_helper.reset_settings_file(self.SETTING)
            return _get_data()
