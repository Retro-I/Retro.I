import json

from helper.Constants import Constants

c = Constants()


class TrebleStepsHelper:
    TREBLE_STEPS_PATH = f"{Constants.settings_path()}/treble-steps.json"

    def get_slider(self):
        with open(self.TREBLE_STEPS_PATH) as file:
            data = json.load(file)

        return data

    def get_min_step(self):
        data = self.get_slider()

        min_step = 999
        for step in data[0]["steps"]:
            if step["step"] < min_step:
                min_step = step["step"]

        return min_step

    def get_max_step(self):
        data = self.get_slider()

        max_step = -999
        for step in data[0]["steps"]:
            if step["step"] > max_step:
                max_step = step["step"]

        return max_step

    def get_gain_for_step(self, step, frequency):
        data = self.get_slider()
        for slider in data:
            if slider["hertz"] == frequency:
                for slider_step in slider["steps"]:
                    if slider_step["step"] == step:
                        return slider_step["value"]

        return 0

    def get_steps_count(self):
        return len(self.get_slider()[0]["steps"])
