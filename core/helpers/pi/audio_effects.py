import json
import subprocess

from core.factories.settings_factories import (
    create_bass_settings,
    create_treble_settings,
)
from core.helpers.base.audio_effects import BaseAudioEffectsHelper
from helper.constants import Constants

c = Constants()


class PiAudioEffectsHelper(BaseAudioEffectsHelper):
    EFFECTS_PATH = Constants.effects_path()

    def __init__(self):
        self.bass_settings = create_bass_settings()
        self.treble_settings = create_treble_settings()

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
        with open(self.EFFECTS_PATH) as file:
            data = json.load(file)
        return data

    def get_bass_value(self):
        config = self.get_config()
        return config["output"]["bass_enhancer#0"]["amount"]

    def get_pitch_value(self):
        config = self.get_config()
        return config["output"]["pitch#0"]["semitones"]

    def update_bass(self, step):
        config = self.get_config()

        for slider in self.bass_settings.get_slider():
            for _, props in config["output"]["equalizer#0"]["left"].items():
                gain = self.bass_settings.get_gain_for_step(
                    step, props["frequency"]
                )
                if props["frequency"] == slider["hertz"]:
                    props["gain"] = gain

            for _, props in config["output"]["equalizer#0"]["right"].items():
                gain = self.bass_settings.get_gain_for_step(
                    step, props["frequency"]
                )
                if props["frequency"] == slider["hertz"]:
                    props["gain"] = gain

        self.write_config(config)
        self.load_effects()

    def update_treble(self, step):
        config = self.get_config()

        for slider in self.treble_settings.get_slider():
            for _, props in config["output"]["equalizer#0"]["left"].items():
                gain = self.treble_settings.get_gain_for_step(
                    step, props["frequency"]
                )
                if props["frequency"] == slider["hertz"]:
                    props["gain"] = gain

            for _, props in config["output"]["equalizer#0"]["right"].items():
                gain = self.treble_settings.get_gain_for_step(
                    step, props["frequency"]
                )
                if props["frequency"] == slider["hertz"]:
                    props["gain"] = gain

        self.write_config(config)
        self.load_effects()

    def write_config(self, config):
        with open(self.EFFECTS_PATH, "w") as file:
            file_data = config
            json.dump(file_data, file, indent=4)

    def load_start_effects(self):
        self.update_bass(0)
        self.update_treble(0)
        self.load_effects()

    def load_effects(self):
        command = ["easyeffects", "-l", "retroi"]
        subprocess.run(command, stdout=subprocess.DEVNULL)
