class BaseAudioEffectsHelper:
    def start(self):
        raise NotImplementedError

    def stop(self):
        raise NotImplementedError

    def get_config(self):
        raise NotImplementedError

    def get_bass_value(self):
        raise NotImplementedError

    def get_pitch_value(self):
        raise NotImplementedError

    def update_bass(self, step):
        raise NotImplementedError

    def update_treble(self, step):
        raise NotImplementedError

    def write_config(self, config):
        raise NotImplementedError

    def load_start_effects(self):
        raise NotImplementedError

    def load_effects(self):
        raise NotImplementedError
