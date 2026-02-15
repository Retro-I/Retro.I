from hardware.base_strip_interface import BaseStripInterface
from helper.Strip import Strip


class PiStripHardware(BaseStripInterface):
    def __init__(self):
        self.strip = Strip()

    def update_sound_strip(self, value):
        self.strip.update_sound_strip(value)

    def update_bass_strip(self, value):
        self.strip.update_bass_strip(value)

    def update_treble_strip(self, value):
        self.strip.update_treble_strip(value)

    def toggle_mute(self, is_mute):
        self.strip.toggle_mute(is_mute)

    def update_strip(self, color):
        self.strip.update_strip(color)

    def toggle_strip(self, event):
        self.strip.toggle_strip(event)

    def change_brightness(self, value, save=True):
        self.strip.change_brightness(value, save)

    def disable(self, save=True):
        self.strip.disable(save)
