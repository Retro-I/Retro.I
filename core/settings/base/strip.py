class BaseStripSettings:
    def is_strip_active(self) -> bool:
        raise NotImplementedError

    def get_led_length(self) -> int:
        raise NotImplementedError

    def get_curr_brightness(self) -> float:
        raise NotImplementedError

    def update_settings(self, is_active, brightness, length):
        raise NotImplementedError