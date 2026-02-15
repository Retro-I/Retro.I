from core.helpers.base.player import BasePlayerHelper
from helper.PageState import PageState


class WebPlayerHelper(BasePlayerHelper):
    def play_src(self, src):
        self.pause()
        PageState.audio.release()
        PageState.audio.src = src
        self.play()

    def play(self):
        PageState.audio.play()

    def pause(self):
        PageState.audio.pause()

    def startup_sound(self):
        pass

    def shutdown_sound(self):
        pass

    def bluetooth_connected(self):
        pass

    def bluetooth_disconnected(self):
        pass
