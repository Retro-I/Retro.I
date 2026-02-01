import os
import shutil
import sys
import tempfile
import unittest
from unittest import mock
from unittest.mock import patch

from helper.AudioEffects import AudioEffects
from helper.BassStepsHelper import BassStepsHelper
from helper.Constants import Constants
from helper.DeveloperModeHelper import DeveloperModeHelper
from helper.PartyModeHelper import PartyModeHelper
from helper.RevisionHelper import RevisionHelper
from helper.ScrollbarSettingsHelper import ScrollbarSettingsHelper
from helper.SecuredModeSettingsHelper import SecuredModeSettingsHelper
from helper.Sounds import Sounds
from helper.SplashscreenHelper import SplashscreenHelper
from helper.StartupErrorHelper import StartupErrorHelper
from helper.StripSettingsHelper import StripSettingsHelper
from helper.ThemeHelper import ThemeHelper
from helper.TrebleStepsHelper import TrebleStepsHelper


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

        self.test_dir = self._create_temp_files(
            src_dir="./settings", dst_dir=f"{tempfile.mkdtemp()}/settings"
        )

        self.test_dir_default = self._create_temp_files(
            src_dir="./settings", dst_dir=f"{tempfile.mkdtemp()}/settings"
        )

        self.test_effects_path = self._create_temp_files(
            src_dir="./assets/effects", dst_dir=f"{tempfile.mkdtemp()}/effects"
        )

        self.test_splashscreen_path = self._create_temp_files(
            src_dir="./assets/splashscreen",
            dst_dir=f"{tempfile.mkdtemp()}/splashscreen",
        )

        Constants.settings_path = staticmethod(lambda: self.test_dir)
        Constants.default_settings_path = staticmethod(
            lambda: self.test_dir_default
        )
        Constants.effects_path = staticmethod(
            lambda: f"{self.test_effects_path}/retroi.json"
        )
        Constants.splashscreen_path = staticmethod(
            lambda: self.test_splashscreen_path
        )

        self.assertTrue(os.path.exists(self.test_dir))
        self.assertTrue(os.path.exists(f"{self.test_dir}/schemas"))
        self.assertTrue(os.path.exists(f"{self.test_effects_path}/retroi.json"))

        self.audio_settings_dispatcher = patch(
            "helper.Audio.Audio.unmute", return_value=None
        )
        self.audio_settings_dispatcher.start()

        self.load_effects_dispatcher = patch(
            "helper.AudioEffects.AudioEffects.load_effects", return_value=None
        )
        self.load_effects_dispatcher.start()

        self.patcher_current = patch.object(
            RevisionHelper, "get_current_revision", return_value="develop"
        )
        self.patcher_local = patch.object(
            RevisionHelper, "get_local_branches", return_value=["develop"]
        )
        self.patcher_remote = patch.object(
            RevisionHelper, "get_branches", return_value=[{"name": "develop"}]
        )

        self.mock_current_revision = self.patcher_current.start()
        self.mock_local_branches = self.patcher_local.start()
        self.mock_remote_branches = self.patcher_remote.start()

        self.addCleanup(self.patcher_current.stop)
        self.addCleanup(self.patcher_local.stop)
        self.addCleanup(self.patcher_remote.stop)

        gpio_settings_path = f"{self.test_dir}/gpio-pin-mapping.json"
        sounds_settings_path = f"{self.test_dir}/favorite-sounds.json"
        radio_stations_path = f"{self.test_dir}/radio-stations.json"
        audio_settings_path = f"{self.test_dir}/audio-settings.json"
        strip_settings_path = f"{self.test_dir}/strip-settings.json"
        theme_settings_path = f"{self.test_dir}/theme-mode-settings.json"
        scrollbar_settings_path = f"{self.test_dir}/scrollbar-settings.json"
        party_mode_path = f"{self.test_dir}/party-mode.json"
        secured_mode_settings_path = (
            f"{self.test_dir}/secured-mode-settings.json"
        )
        developer_mode_settings_path = (
            f"{self.test_dir}/developer-mode-settings.json"
        )
        startup_error_helper = f"{self.test_dir}/startup-error.json"
        bass_steps_path = f"{self.test_dir}/bass-steps.json"
        treble_steps_path = f"{self.test_dir}/treble-steps.json"
        effects_path = f"{self.test_effects_path}/retroi.json"

        Audio.AUDIO_SETTINGS_PATH = audio_settings_path
        GpioHelper.GPIO_SETTINGS_PATH = gpio_settings_path
        Sounds.FAV_SOUNDS_PATH = sounds_settings_path
        Stations.STATIONS_SETTINGS_PATH = radio_stations_path
        StripSettingsHelper.STRIP_SETTINGS_PATH = strip_settings_path
        ThemeHelper.THEME_SETTINGS_PATH = theme_settings_path
        ScrollbarSettingsHelper.SCROLLBAR_SETTINGS_PATH = (
            scrollbar_settings_path
        )
        SecuredModeSettingsHelper.SECURED_MODE_PATH = secured_mode_settings_path
        StartupErrorHelper.STARTUP_ERROR_PATH = startup_error_helper
        BassStepsHelper.BASS_STEPS_PATH = bass_steps_path
        TrebleStepsHelper.TREBLE_STEPS_PATH = treble_steps_path
        AudioEffects.EFFECTS_PATH = effects_path
        DeveloperModeHelper.SETTINGS_PATH = developer_mode_settings_path
        PartyModeHelper.SETTINGS_PATH = party_mode_path

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
        self.bass_steps_helper = BassStepsHelper()
        self.treble_steps_helper = TrebleStepsHelper()
        self.audio_effects = AudioEffects()
        self.splashscreen_helper = SplashscreenHelper()
        self.developer_mode_settings_helper = DeveloperModeHelper()
        self.party_mode_helper = PartyModeHelper()

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
            target_root = (
                os.path.join(dst_dir, rel_path) if rel_path != "." else dst_dir
            )

            # Create missing directories
            os.makedirs(target_root, exist_ok=True)

            # Copy files in this directory
            for file in files:
                src_file = os.path.join(root, file)
                dst_file = os.path.join(target_root, file)
                shutil.copy2(src_file, dst_file)

        return dst_dir
