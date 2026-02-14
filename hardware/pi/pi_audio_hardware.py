from hardware.base_audio_interface import BaseAudioInterface
from helper.Audio import Audio


class PiAudioHardware(BaseAudioInterface):
    def __init__(self):
        self.audio = Audio()

    def init_sound(self):
        self.audio.init_sound()

    def set_volume(self, value):
        self.audio.set_volume(value)

    def get_volume(self):
        return self.audio.get_volume()

    def toggle_mute(self):
        self.audio.toggle_mute()

    def is_mute(self):
        self.audio.is_mute()

    def play_src(self, src):
        self.audio.play_src(src)

    def pause(self):
        self.audio.pause()

    def startup_sound(self):
        self.audio.startup_sound()

    def shutdown_sound(self):
        self.audio.shutdown_sound()

    def bluetooth_connected(self):
        self.audio.bluetooth_connected()

    def bluetooth_disconnected(self):
        self.audio.bluetooth_disconnected()

    def get_audio_sinks(self) -> list[dict]:
        return self.audio.get_audio_sinks()

    def get_current_audio_sink(self) -> dict:
        return self.audio.get_current_audio_sink()

    def set_audio_output(self, sink_id: str):
        self.audio.set_audio_output(sink_id)

    def play_toast(self):
        self.audio.play_toast()

    def play_sound_board(self, src):
        self.audio.play_sound_board(src)

    def is_default_station_autoplay_enabled(self) -> bool:
        return self.audio.is_default_station_autoplay_enabled()

    def toggle_default_station_autoplay(self):
        self.audio.toggle_default_station_autoplay()

    def get_default_volume(self) -> int:
        self.audio.get_default_volume()

    def set_default_volume(self, value):
        self.audio.set_default_volume(value)

    def get_volume_step(self) -> int:
        self.audio.get_volume_step()

    def set_volume_step(self, value):
        self.audio.set_volume_step(value)
