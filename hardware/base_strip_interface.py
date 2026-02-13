class BaseStripInterface:
    def update_sound_strip(self, value):
        raise NotImplementedError("implement in subclass")

    def update_bass_strip(self, value):
        raise NotImplementedError("implement in subclass")

    def update_treble_strip(self, value):
        raise NotImplementedError("implement in subclass")

    def toggle_mute(self, is_mute):
        raise NotImplementedError("implement in subclass")

    def update_strip(self, color):
        raise NotImplementedError("implement in subclass")

    def toggle_strip(self, event):
        raise NotImplementedError("implement in subclass")

    def change_brightness(self, value, save=True):
        raise NotImplementedError("implement in subclass")

    def disable(self, save=True):
        raise NotImplementedError("implement in subclass")
