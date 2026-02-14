import logging

from hardware.base_audio_interface import BaseAudioInterface

logger = logging.getLogger(__name__)


class WebAudioHardware(BaseAudioInterface):
    def init_sound(self):
        logger.debug("[MOCK AUDIO] init_sound")

    def set_volume(self, value):
        logger.debug("[MOCK AUDIO] set_volume")

    def get_volume(self):
        logger.debug("[MOCK AUDIO] get_volume")

    def toggle_mute(self):
        logger.debug("[MOCK AUDIO] toggle_mute")

    def is_mute(self):
        logger.debug("[MOCK AUDIO] is_mute")

    def play_src(self, src):
        logger.debug("[MOCK AUDIO] play_src")

    def pause(self):
        logger.debug("[MOCK AUDIO] pause")

    def startup_sound(self):
        logger.debug("[MOCK AUDIO] startup_sound")

    def shutdown_sound(self):
        logger.debug("[MOCK AUDIO] shutdown_sound")

    def bluetooth_connected(self):
        logger.debug("[MOCK AUDIO] bluetooth_connected")

    def bluetooth_disconnected(self):
        logger.debug("[MOCK AUDIO] bluetooth_disconnected")

    def get_audio_sinks(self) -> list[dict]:
        logger.debug("[MOCK AUDIO] get_audio_sinks")

    def get_current_audio_sink(self) -> dict:
        logger.debug("[MOCK AUDIO] get_current_audio_sink")

    def set_audio_output(self, sink_id: str):
        logger.debug("[MOCK AUDIO] set_audio_output")

    def play_toast(self):
        logger.debug("[MOCK AUDIO] play_toast")

    def play_sound_board(self, src):
        logger.debug("[MOCK AUDIO] play_sound_board")

    def is_default_station_autoplay_enabled(self) -> bool:
        logger.debug("[MOCK AUDIO] is_default_station_autoplay_enabled")

    def toggle_default_station_autoplay(self):
        logger.debug("[MOCK AUDIO] toggle_default_station_autoplay")

    def get_default_volume(self) -> int:
        logger.debug("[MOCK AUDIO] get_default_volume")

    def set_default_volume(self, value):
        logger.debug("[MOCK AUDIO] set_default_volume")

    def get_volume_step(self) -> int:
        logger.debug("[MOCK AUDIO] get_volume_step")

    def set_volume_step(self, value):
        logger.debug("[MOCK AUDIO] set_volume_step")