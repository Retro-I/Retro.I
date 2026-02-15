import logging

from hardware.base_strip_interface import BaseStripInterface

logger = logging.getLogger(__name__)


class WebStripHardware(BaseStripInterface):
    def update_sound_strip(self, value):
        logger.debug("[MOCK LED] update_sound_strip")

    def update_bass_strip(self, value):
        logger.debug("[MOCK LED] update_bass_strip")

    def update_treble_strip(self, value):
        logger.debug("[MOCK LED] update_treble_strip")

    def toggle_mute(self, is_mute):
        logger.debug("[MOCK LED] toggle_mute")

    def update_strip(self, color):
        logger.debug("[MOCK LED] update_strip")

    def toggle_strip(self, event):
        logger.debug("[MOCK LED] toggle_strip")

    def change_brightness(self, value, save=True):
        logger.debug("[MOCK LED] change_brightness")

    def disable(self, save=True):
        logger.debug("[MOCK LED] disable")
