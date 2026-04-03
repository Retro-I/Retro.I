class BaseStepsSettings:
    def get_slider(self):
        raise NotImplementedError

    def get_min_step(self):
        raise NotImplementedError

    def get_max_step(self):
        raise NotImplementedError

    def get_gain_for_step(self, step, frequency):
        raise NotImplementedError

    def get_steps_count(self):
        raise NotImplementedError
