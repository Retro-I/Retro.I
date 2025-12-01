import os
import shutil
import sys
import tempfile
import unittest
from unittest import mock
from unittest.mock import patch

from helper.ScrollbarSettingsHelper import ScrollbarSettingsHelper
from helper.SecuredModeSettingsHelper import SecuredModeSettingsHelper
from helper.Sounds import Sounds
from helper.StartupErrorHelper import StartupErrorHelper
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
        from helper.SettingsSyncHelper import SettingsSyncHelper
        from helper.Stations import Stations

        self.audio_settings_dispatcher = patch("helper.Audio.Audio.init_sound", return_value=None)
        self.audio_settings_dispatcher.start()

        self.audio_helper = Audio()
        self.gpio_helper = GpioHelper()
        self.settings_sync_helper = SettingsSyncHelper()
        self.sounds_helper = Sounds()
        self.stations = Stations()
        self.strip_settings_helper = StripSettingsHelper()
        self.theme_helper = ThemeHelper()
        self.scrollbar_settings_helper = ScrollbarSettingsHelper()
        self.secured_mode_settings = SecuredModeSettingsHelper()
        self.startup_error_helper = StartupErrorHelper()

        self.test_dir = tempfile.mkdtemp()
        self.base_dir = self._create_temp_files(
            src_dir="./settings", dst_dir=f"{self.test_dir}/settings"
        )

        self.default_settings_patcher = patch(
            "helper.Constants.Constants.default_settings_path", return_value="./settings"
        )
        self.default_settings_patcher.start()

        self.settings_patcher = patch(
            "helper.Constants.Constants.settings_path", return_value=self.base_dir
        )
        self.settings_patcher.start()
        self.assertTrue(os.path.exists(self.base_dir))
        self.assertTrue(os.path.exists(f"{self.base_dir}/schemas"))

        gpio_settings_path = f"{self.base_dir}/gpio-pin-mapping.json"
        sounds_settings_path = f"{self.base_dir}/favorite-sounds.json"
        radio_stations_path = f"{self.base_dir}/radio-stations.json"
        audio_settings_path = f"{self.base_dir}/audio-settings.json"
        strip_settings_path = f"{self.base_dir}/strip-settings.json"
        theme_settings_path = f"{self.base_dir}/theme-mode-settings.json"
        scrollbar_settings_path = f"{self.base_dir}/scrollbar-settings.json"
        secured_mode_settings_path = f"{self.base_dir}/secured-mode-settings.json"
        startup_error_helper = f"{self.base_dir}/startup-error.json"

        self.audio_helper.AUDIO_SETTINGS_PATH = audio_settings_path
        self.gpio_helper.GPIO_SETTINGS_PATH = gpio_settings_path
        self.sounds_helper.FAV_SOUNDS_PATH = sounds_settings_path
        self.stations.STATIONS_SETTINGS_PATH = radio_stations_path
        self.strip_settings_helper.STRIP_SETTINGS_PATH = strip_settings_path
        self.theme_helper.THEME_SETTINGS_PATH = theme_settings_path
        self.scrollbar_settings_helper.SCROLLBAR_SETTINGS_PATH = scrollbar_settings_path
        self.secured_mode_settings.SECURED_MODE_PATH = secured_mode_settings_path
        self.startup_error_helper.STARTUP_ERROR_PATH = startup_error_helper

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
            target_root = os.path.join(dst_dir, rel_path) if rel_path != "." else dst_dir

            # Create missing directories
            os.makedirs(target_root, exist_ok=True)

            # Copy files in this directory
            for file in files:
                src_file = os.path.join(root, file)
                dst_file = os.path.join(target_root, file)
                shutil.copy2(src_file, dst_file)

        return dst_dir
