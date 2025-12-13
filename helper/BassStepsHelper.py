import json

from helper.Constants import Constants

c = Constants()


class BassStepsHelper:
    BASS_STEPS_PATH = f"{Constants.settings_path()}/bass-steps.json"

    def get_slider(self):
        with open(self.BASS_STEPS_PATH) as file:
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
