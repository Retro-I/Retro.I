import json

from helper.Constants import Constants
from helper.SettingsSyncHelper import SettingsSyncHelper

c = Constants()
settings_sync_helper = SettingsSyncHelper()


class GpioHelper:
    SETTING = "gpio-pin-mapping.json"
    GPIO_SETTINGS_PATH = f"{Constants.settings_path()}/{SETTING}"

    def get_mappings(self) -> dict:
        def _get_data():
            with open(self.GPIO_SETTINGS_PATH) as file:
                data = json.load(file)
                return data

        try:
            return _get_data()
        except Exception:
            settings_sync_helper.repair_settings_file(self.SETTING)
            return _get_data()

    def rotary_volume_up(self) -> int:
        return self.get_mappings()["ROTARY_VOLUME_UP"]

    def rotary_volume_down(self) -> int:
        return self.get_mappings()["ROTARY_VOLUME_DOWN"]

    def rotary_volume_press(self) -> int:
        return self.get_mappings()["ROTARY_VOLUME_PRESS"]

    def rotary_bass_up(self) -> int:
        return self.get_mappings()["ROTARY_BASS_UP"]

    def rotary_bass_down(self) -> int:
        return self.get_mappings()["ROTARY_BASS_DOWN"]

    def rotary_treble_up(self) -> int:
        return self.get_mappings()["ROTARY_TREBLE_UP"]

    def rotary_treble_down(self) -> int:
        return self.get_mappings()["ROTARY_TREBLE_DOWN"]

    def start_party_button(self) -> int:
        return self.get_mappings()["START_PARTY_MODE_BUTTON"]

    def shutdown_button(self) -> int:
        return self.get_mappings()["SHUTDOWN_BUTTON"]
