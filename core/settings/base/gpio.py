from helper.constants import Constants

c = Constants()


class BaseGpioSettings:
    def get_mappings(self) -> dict:
        raise NotImplementedError

    def rotary_volume_up(self) -> int:
        raise NotImplementedError

    def rotary_volume_down(self) -> int:
        raise NotImplementedError

    def rotary_volume_press(self) -> int:
        raise NotImplementedError

    def rotary_bass_up(self) -> int:
        raise NotImplementedError

    def rotary_bass_down(self) -> int:
        raise NotImplementedError

    def rotary_treble_up(self) -> int:
        raise NotImplementedError

    def rotary_treble_down(self) -> int:
        raise NotImplementedError

    def start_party_button(self) -> int:
        raise NotImplementedError

    def shutdown_button(self) -> int:
        raise NotImplementedError
