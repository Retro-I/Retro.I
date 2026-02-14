class BaseStripInterface:
    def update_sound_strip(self, value):
        raise NotImplementedError

    def update_bass_strip(self, value):
        raise NotImplementedError

    def update_treble_strip(self, value):
        raise NotImplementedError

    def toggle_mute(self, is_mute):
        raise NotImplementedError

    def update_strip(self, color):
        raise NotImplementedError

    def toggle_strip(self, event):
        raise NotImplementedError

    def change_brightness(self, value, save=True):
        raise NotImplementedError

    def disable(self, save=True):
        raise NotImplementedError
