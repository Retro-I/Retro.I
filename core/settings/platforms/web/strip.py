from core.settings.base.strip import BaseStripSettings


class WebStripSettings(BaseStripSettings):
    def is_strip_active(self) -> bool:
        return False

    def get_led_length(self) -> int:
        return 0

    def get_curr_brightness(self) -> float:
        return 0

    def update_settings(self, is_active, brightness, length):
        pass
