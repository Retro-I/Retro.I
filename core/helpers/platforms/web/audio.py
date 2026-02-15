from core.helpers.base.audio import BaseAudioHelper


class WebAudioHelper(BaseAudioHelper):
    def init_sound(self):
        pass

    def set_volume(self, value):
        pass

    def get_volume(self):
        pass

    def toggle_mute(self):
        pass

    def is_mute(self) -> bool:
        pass

    def get_audio_sinks(self) -> list[dict]:
        return []

    def get_current_audio_sink(self) -> dict:
        return None

    def set_audio_output(self, sink_id: str):
        pass

    def play_toast(self):
        pass

    def play_sound_board(self, src):
        pass

    def is_default_station_autoplay_enabled(self) -> bool:
        pass

    def toggle_default_station_autoplay(self):
        pass

    def get_default_volume(self) -> int:
        return 20

    def set_default_volume(self, value):
        pass

    def get_volume_step(self) -> int:
        return 5

    def set_volume_step(self, value):
        pass
