class BaseStripSettings:
    def is_strip_active(self) -> bool:
        raise NotImplementedError

    def get_led_length(self) -> int:
        raise NotImplementedError

    def get_curr_brightness(self) -> float:
        raise NotImplementedError

    def is_static_color(self) -> bool:
        raise NotImplementedError

    def get_static_color(self) -> str:
        raise NotImplementedError

    def get_strip_settings(self):
        raise NotImplementedError

    def update_settings(
        self,
        is_active: bool | None = None,
        brightness: float | None = None,
        length: int | None = None,
        is_static_color: bool | None = None,
        static_color: str | None = None,
    ):
        raise NotImplementedError
