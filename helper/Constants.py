import os
import random
from pathlib import Path

from appdirs import user_data_dir


class Constants:
    current_radio_station = {}
    current_station_index_to_delete = None
    indicator_refs = []
    current_bass_step = 0
    current_treble_step = 0

    @staticmethod
    def pwd() -> str:
        retroi_dir = os.environ.get("RETROI_DIR")
        if retroi_dir:
            return retroi_dir

        return str(Path(__file__).resolve().parent.parent)

    @staticmethod
    def settings_path() -> str:
        return str(os.path.join(user_data_dir("retroi")))

    @staticmethod
    def default_settings_path() -> str:
        return str(os.path.join(Constants.pwd(), "settings"))

    def sound_path(self):
        return f"{self.pwd()}/assets/sounds"

    def system_sound_path(self):
        return f"{self.pwd()}/assets/system_sounds"

    def toast_path(self):
        return f"{self.pwd()}/assets/toasts"

    def get_button_img(self):
        buttons_path = f"{self.pwd()}/assets/buttons"
        files = [
            f for f in os.listdir(buttons_path) if os.path.isfile(os.path.join(buttons_path, f))
        ]
        return os.path.join(buttons_path, random.choice(files))
