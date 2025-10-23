import json
import os
import subprocess

from helper.Constants import Constants

c = Constants()


class AudioEffects:
    def __init__(self):
        home_dir = os.environ.get("HOME")
        self.effects_path = f"{home_dir}/.config/easyeffects/output/retroi.json"

    def start(self):
        self.stop()
        self.load_start_effects()
        command = ["easyeffects", "--gapplication-service"]
        subprocess.Popen(command, stdout=subprocess.DEVNULL)

    def stop(self):
        command = ["pkill", "-f", "easyeffects"]
        subprocess.run(command, stdout=subprocess.DEVNULL)
        self.load_start_effects()

    def get_config(self):
        f = open(self.effects_path)
        data = json.load(f)
        f.close()
        return data

    def get_bass_value(self):
        config = self.get_config()
        return config["output"]["bass_enhancer#0"]["amount"]

    def get_pitch_value(self):
        config = self.get_config()
        return config["output"]["pitch#0"]["semitones"]

    def update_bass(self, value):
        config = self.get_config()
        config["output"]["bass_enhancer#0"]["amount"] = value

        self.write_config(config)
        self.load_effects()

    def update_pitch(self, value):
        config = self.get_config()
        config["output"]["pitch#0"]["semitones"] = value

        self.write_config(config)
        self.load_effects()

    def write_config(self, config):
        with open(self.effects_path, "w") as file:
            file_data = config
            json.dump(file_data, file, indent=4)

    def load_start_effects(self):
        self.update_bass(0)
        self.update_pitch(0)
        self.load_effects()

    def load_effects(self):
        command = ["easyeffects", "-l", "retroi"]
        subprocess.run(command, stdout=subprocess.DEVNULL)
