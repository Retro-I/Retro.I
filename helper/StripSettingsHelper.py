import json
import re

from helper.Constants import Constants
from helper.SettingsSyncHelper import SettingsSyncHelper

c = Constants()
settings_sync_helper = SettingsSyncHelper()


class StripSettingsHelper:
    SETTING = "strip-settings.json"
    STRIP_SETTINGS_PATH = f"{Constants.settings_path()}/{SETTING}"

    def is_strip_active(self) -> bool:
        settings = self.get_strip_settings()
        return settings["isStripEnabled"]

    def get_led_length(self) -> int:
        settings = self.get_strip_settings()
        return settings["amountLeds"]

    def get_curr_brightness(self) -> float:
        settings = self.get_strip_settings()
        return settings["brightness"]

    def is_static_color(self) -> bool:
        settings = self.get_strip_settings()
        return settings["isStaticColor"]

    def get_static_color(self) -> str:
        settings = self.get_strip_settings()
        return settings["staticColor"].upper()

    def get_strip_settings(self):
        def _get_data():
            with open(self.STRIP_SETTINGS_PATH) as file:
                data = json.load(file)
                return data

        try:
            return _get_data()
        except Exception:
            settings_sync_helper.reset_settings_file(self.SETTING)
            return _get_data()

    def update_settings(
        self,
        is_active: bool | None = None,
        brightness: float | None = None,
        length: int | None = None,
        is_static_color: bool | None = None,
        static_color: str | None = None,
    ):
        _is_active = (
            is_active if is_active is not None else self.is_strip_active()
        )
        _brightness = (
            brightness if brightness is not None else self.get_curr_brightness()
        )
        _length = length if length is not None else self.get_led_length()
        _is_static_color = (
            is_static_color
            if is_static_color is not None
            else self.is_static_color()
        )

        regex = "^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$"
        p = re.compile(regex)
        if static_color is None:
            _static_color = self.get_static_color()
        elif re.search(p, static_color):
            _static_color = static_color
        else:
            _static_color = self.get_static_color()

        data = self.get_strip_settings()
        data["isStripEnabled"] = _is_active
        data["brightness"] = _brightness
        data["amountLeds"] = _length
        data["isStaticColor"] = _is_static_color
        data["staticColor"] = _static_color

        with open(self.STRIP_SETTINGS_PATH, "r+") as file:
            file.seek(0)
            json.dump(data, file, indent=4)
            file.truncate()
