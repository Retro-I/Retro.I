class BasePlayerHelper:
    def play_src(self, src):
        raise NotImplementedError

    def play(self):
        raise NotImplementedError

    def pause(self):
        raise NotImplementedError

    def _play_sound(self, src):
        raise NotImplementedError

    def startup_sound(self):
        raise NotImplementedError

    def shutdown_sound(self):
        raise NotImplementedError

    def bluetooth_connected(self):
        raise NotImplementedError

    def bluetooth_disconnected(self):
        raise NotImplementedError
