import os
import shutil
import sys
import tempfile
import unittest
from unittest import mock
from unittest.mock import patch

from helper.Sounds import Sounds
from helper.StripSettingsHelper import StripSettingsHelper
from helper.ThemeHelper import ThemeHelper


class BaseTest(unittest.TestCase):
    @mock.patch.dict(
        sys.modules,
        {
            "alsaaudio": mock.MagicMock(),
            "vlc": mock.MagicMock(),
            "playsound3": mock.MagicMock(),
            "cairosvg": mock.MagicMock(),
            "numpy": mock.MagicMock(),
            "joblib": mock.MagicMock(),
            "sklearn.cluster": mock.MagicMock(),
            "board": mock.MagicMock(),
            "digitalio": mock.MagicMock(),
            "neopixel_write": mock.MagicMock(),
            "adafruit_pixelbuf": mock.MagicMock(),
            "neopixel": mock.MagicMock(),
            "rainbowio": mock.MagicMock(),
        },
    )
    def setUp(self):
        from helper.Audio import Audio
        from helper.GpioHelper import GpioHelper
        from helper.Stations import Stations

        self.test_dir = tempfile.mkdtemp()

        self.gpio_helper = GpioHelper()
        self.sounds_helper = Sounds()
        self.stations = Stations()
        self.strip_settings_helper = StripSettingsHelper()
        self.theme_helper = ThemeHelper()

        gpio_settings_path = self._create_temp_file(
            actual="./settings/gpio-pin-mapping.json",
            target="gpio_pin_mapping_data_copy.json",
        )
        sounds_settings_path = self._create_temp_file(
            actual="./settings/favorite-sounds.json", target="favorite_sounds_data_copy.json"
        )
        radion_stations_path = self._create_temp_file(
            actual="./settings/radio-stations.json", target="radio_stations_data_copy.json"
        )
        audio_settings_path = self._create_temp_file(
            actual="./settings/audio-settings.json", target="audio_settings_data_copy.json"
        )
        strip_settings_path = self._create_temp_file(
            actual="./settings/strip-settings.json", target="strip_settings_data_copy.json"
        )
        theme_settings_path = self._create_temp_file(
            actual="./settings/theme-mode-settings.json",
            target="theme_mode_settings_data_copy.json",
        )

        self.gpio_helper.GPIO_SETTINGS_PATH = gpio_settings_path
        self.sounds_helper.FAV_SOUNDS_PATH = sounds_settings_path
        self.stations.STATIONS_SETTINGS_PATH = radion_stations_path
        self.stations.AUDIO_SETTINGS_PATH = audio_settings_path
        self.strip_settings_helper.STRIP_SETTINGS_PATH = strip_settings_path
        self.theme_helper.THEME_SETTINGS_PATH = theme_settings_path

        with patch.object(Audio, "AUDIO_SETTINGS_PATH", audio_settings_path):
            with mock.patch.object(Audio, "init_sound"):
                self.audio_helper = Audio()
                self.audio_helper.AUDIO_SETTINGS_PATH = audio_settings_path

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def _create_temp_file(self, actual: str, target: str) -> str:
        self.settings_file = os.path.join(actual)
        self.temp_file = os.path.join(self.test_dir, target)
        shutil.copy(self.settings_file, self.temp_file)

        return self.temp_file
