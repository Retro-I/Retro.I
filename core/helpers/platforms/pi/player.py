from core.helpers.base.player import BasePlayerHelper
from helper.Player import Player


class PiPlayerHelper(BasePlayerHelper):
    def __init__(self):
        self.helper = Player()

    def play_src(self, src):
        self.helper.play_src(src)

    def play(self):
        self.helper.play()

    def pause(self):
        self.helper.pause()

    def startup_sound(self):
        self.helper.startup_sound()

    def shutdown_sound(self):
        self.helper.shutdown_sound()

    def bluetooth_connected(self):
        self.helper.bluetooth_connected()

    def bluetooth_disconnected(self):
        self.helper.bluetooth_disconnected()
