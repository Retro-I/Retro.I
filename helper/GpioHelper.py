import json

from helper.Constants import Constants

c = Constants()


class GpioHelper:
    GPIO_SETTINGS_PATH = f"{c.settings_path()}/gpio-pin-mapping.json"

    def get_mappings(self) -> dict:
        with open(self.GPIO_SETTINGS_PATH) as file:
            data = json.load(file)
            return data

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

    def rotary_pitch_up(self) -> int:
        return self.get_mappings()["ROTARY_PITCH_UP"]

    def rotary_pitch_down(self) -> int:
        return self.get_mappings()["ROTARY_PITCH_DOWN"]
