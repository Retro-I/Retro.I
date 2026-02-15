class BaseAudioHelper:
    def init_sound(self):
        raise NotImplementedError

    def set_volume(self, value):
        raise NotImplementedError

    def get_volume(self):
        raise NotImplementedError

    def toggle_mute(self):
        raise NotImplementedError

    def is_mute(self) -> bool:
        raise NotImplementedError

    def get_audio_sinks(self) -> list[dict]:
        raise NotImplementedError

    def get_current_audio_sink(self) -> dict:
        raise NotImplementedError

    def set_audio_output(self, sink_id: str):
        raise NotImplementedError

    def play_toast(self):
        raise NotImplementedError

    def play_sound_board(self, src):
        raise NotImplementedError

    def is_default_station_autoplay_enabled(self) -> bool:
        raise NotImplementedError

    def toggle_default_station_autoplay(self):
        raise NotImplementedError

    def get_default_volume(self) -> int:
        raise NotImplementedError

    def set_default_volume(self, value):
        raise NotImplementedError

    def get_volume_step(self) -> int:
        raise NotImplementedError

    def set_volume_step(self, value):
        raise NotImplementedError
