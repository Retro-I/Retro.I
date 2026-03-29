from core.settings.base.strip import BaseStripSettings
from helper.strip_settings_helper import StripSettingsHelper


class PiStripSettings(BaseStripSettings):
    def __init__(self):
        self.settings = StripSettingsHelper()

    def is_strip_active(self) -> bool:
        return self.settings.is_strip_active()

    def get_led_length(self) -> int:
        return self.settings.get_led_length()

    def get_curr_brightness(self) -> float:
        return self.settings.get_curr_brightness()

    def is_static_color(self) -> bool:
        return self.settings.is_static_color()

    def get_static_color(self) -> str:
        return self.settings.get_static_color()

    def update_settings(self, is_active, brightness, length):
        self.settings.update_settings(is_active, brightness, length)
