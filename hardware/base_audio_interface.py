class BaseAudioInterface:
    def init_sound(self):
        raise NotImplementedError("implement in subclass")

    def set_volume(self, value):
        raise NotImplementedError("implement in subclass")

    def get_volume(self):
        raise NotImplementedError("implement in subclass")

    def toggle_mute(self):
        raise NotImplementedError("implement in subclass")

    def is_mute(self):
        raise NotImplementedError("implement in subclass")

    def play_src(self, src):
        raise NotImplementedError("implement in subclass")

    def pause(self):
        raise NotImplementedError("implement in subclass")

    def startup_sound(self):
        raise NotImplementedError("implement in subclass")

    def shutdown_sound(self):
        raise NotImplementedError("implement in subclass")

    def bluetooth_connected(self):
        raise NotImplementedError("implement in subclass")

    def bluetooth_disconnected(self):
        raise NotImplementedError("implement in subclass")

    def get_audio_sinks(self) -> list[dict]:
        raise NotImplementedError("implement in subclass")

    def get_current_audio_sink(self) -> dict:
        raise NotImplementedError("implement in subclass")

    def set_audio_output(self, sink_id: str):
        raise NotImplementedError("implement in subclass")

    def play_toast(self):
        raise NotImplementedError("implement in subclass")

    def play_sound_board(self, src):
        raise NotImplementedError("implement in subclass")

    def is_default_station_autoplay_enabled(self) -> bool:
        raise NotImplementedError("implement in subclass")

    def toggle_default_station_autoplay(self):
        raise NotImplementedError("implement in subclass")

    def get_default_volume(self) -> int:
        raise NotImplementedError("implement in subclass")

    def set_default_volume(self, value):
        raise NotImplementedError("implement in subclass")

    def get_volume_step(self) -> int:
        raise NotImplementedError("implement in subclass")

    def set_volume_step(self, value):
        raise NotImplementedError("implement in subclass")
