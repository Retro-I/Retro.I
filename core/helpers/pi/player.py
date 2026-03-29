import mpv

from core.helpers.base.player import BasePlayerHelper
from helper.constants import Constants

c = Constants()


class PiPlayerHelper(BasePlayerHelper):
    player = mpv.MPV(ytdl=True)
    current_sound = ""

    def play_src(self, src):
        try:
            self.pause()
        except Exception:
            print("Fehler beim abspielen des Radiosenders")
        PiPlayerHelper.current_sound = src
        self.play()

    def play(self):
        PiPlayerHelper.player.play(PiPlayerHelper.current_sound)

    def pause(self):
        PiPlayerHelper.player.stop()

    def _play_sound(self, src):
        PiPlayerHelper.current_sound = src
        self.play()

    def startup_sound(self):
        self._play_sound(f"{c.system_sound_path()}/startup.mp3")

    def shutdown_sound(self):
        self.pause()
        self._play_sound(f"{c.system_sound_path()}/shutdown.mp3")

    def bluetooth_connected(self):
        self._play_sound(f"{c.system_sound_path()}/bluetooth_connected.mp3")

    def bluetooth_disconnected(self):
        self._play_sound(f"{c.system_sound_path()}/bluetooth_disconnected.mp3")
