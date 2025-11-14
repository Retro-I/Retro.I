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
        from helper.SettingsSyncHelper import SettingsSyncHelper

        self.gpio_helper = GpioHelper()
        self.settings_sync_helper = SettingsSyncHelper()
        self.sounds_helper = Sounds()
        self.stations = Stations()
        self.strip_settings_helper = StripSettingsHelper()
        self.theme_helper = ThemeHelper()

        self.test_dir = tempfile.mkdtemp()
        self.patcher = patch(
            "helper.Constants.Constants.default_settings_path",
            return_value=self.test_dir
        )
        self.patcher.start()

        self.base_dir = self._create_temp_files(src_dir="./settings", dst_dir=f"{self.test_dir}/settings")
        self.assertTrue(os.path.exists(self.base_dir))
        self.assertTrue(os.path.exists(f"{self.base_dir}/templates"))

        gpio_settings_path = f"{self.base_dir}/gpio-pin-mapping.json"
        sounds_settings_path = f"{self.base_dir}/favorite-sounds.json"
        radio_stations_path = f"{self.base_dir}/radio-stations.json"
        audio_settings_path = f"{self.base_dir}/audio-settings.json"
        strip_settings_path = f"{self.base_dir}/strip-settings.json"
        theme_settings_path = f"{self.base_dir}/theme-mode-settings.json"

        self.gpio_helper.GPIO_SETTINGS_PATH = gpio_settings_path
        self.sounds_helper.FAV_SOUNDS_PATH = sounds_settings_path
        self.stations.STATIONS_SETTINGS_PATH = radio_stations_path
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
        os.makedirs(os.path.dirname(target), exist_ok=True)
        self.settings_file = os.path.join(actual)
        self.temp_file = os.path.join(self.test_dir, target.replace("/", "/"))
        shutil.copytree(self.settings_file, self.temp_file)

        return self.temp_file

    def _create_temp_files(self, src_dir: str, dst_dir: str) -> str:
        for root, dirs, files in os.walk(src_dir):

            # Compute relative path inside the tree
            rel_path = os.path.relpath(root, src_dir)
            target_root = os.path.join(dst_dir, rel_path) if rel_path != '.' else dst_dir

            # Create missing directories
            os.makedirs(target_root, exist_ok=True)

            # Copy files in this directory
            for file in files:
                src_file = os.path.join(root, file)
                dst_file = os.path.join(target_root, file)
                shutil.copy2(src_file, dst_file)

        return dst_dir
