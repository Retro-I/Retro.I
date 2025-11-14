import os
import shutil
import sys
import tempfile
import unittest
from unittest import mock


# TODO - fix this with refactoring and extract scrollbar settings from system_helper
@unittest.skip
class TestScrollbarSettings(unittest.TestCase):
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
        self.test_dir = tempfile.mkdtemp()

        self.scrollbar_settings_file = os.path.join("./settings/scrollbar-settings.json")
        self.startup_error_file = os.path.join("./settings/startup-error.json")
        self.secured_mode_settings_file = os.path.join("./settings/secured-mode-settings.json")

        self.scrollbar_settings_temp_file = os.path.join(
            self.test_dir, "scrollbar_settings_data_copy.json"
        )
        self.startup_error_temp_file = os.path.join(self.test_dir, "startup_error_data_copy.json")
        self.secured_mode_settings_temp_file = os.path.join(
            self.test_dir, "secured_mode_settings_data_copy.json"
        )

        shutil.copy(self.scrollbar_settings_file, self.scrollbar_settings_temp_file)
        shutil.copy(self.startup_error_file, self.startup_error_temp_file)
        shutil.copy(self.secured_mode_settings_file, self.secured_mode_settings_temp_file)

        from helper.SystemHelper import SystemHelper

        with mock.patch.object(SystemHelper, "strip", mock.MagicMock()):
            self.system_helper = SystemHelper()

            self.system_helper.SCROLLBAR_SETTINGS_PATH = self.scrollbar_settings_temp_file
            self.system_helper.STARTUP_ERROR_PATH = self.startup_error_file
            self.system_helper.SECURED_MODE_SETTINGS_PATH = self.secured_mode_settings_temp_file

    @mock.patch("helper.Strip.Strip")
    def test_default_settings(self, _mock):
        actual = self.system_helper.is_scrollbar_enabled()
        self.assertFalse(actual)

    def test_toggle_scrollbar_enabled(self):
        actual = self.system_helper.is_scrollbar_enabled()
        self.assertFalse(actual)

        self.system_helper.toggle_scrollbar_enabled()
        actual = self.system_helper.is_scrollbar_enabled()
        self.assertTrue(actual)

        self.system_helper.toggle_scrollbar_enabled()
        actual = self.system_helper.is_scrollbar_enabled()
        self.assertFalse(actual)


@unittest.skip
class TestStartupError(unittest.TestCase):

    @mock.patch.dict(sys.modules, {"alsaaudio": mock.MagicMock()})
    @mock.patch.dict(sys.modules, {"vlc": mock.MagicMock()})
    @mock.patch.dict(sys.modules, {"playsound3": mock.MagicMock()})
    @mock.patch.dict(sys.modules, {"cairosvg": mock.MagicMock()})
    @mock.patch.dict(sys.modules, {"numpy": mock.MagicMock()})
    @mock.patch.dict(sys.modules, {"joblib": mock.MagicMock()})
    @mock.patch.dict(sys.modules, {"sklearn.cluster": mock.MagicMock()})
    def setUp(self):
        from helper.SystemHelper import SystemHelper

        self.system_helper = SystemHelper()
        self.test_dir = tempfile.mkdtemp()

        self.scrollbar_settings_file = os.path.join("./settings/startup-error.json")

        self.scrollbar_settings_temp_file = os.path.join(
            self.test_dir, "scrollbar_settings_data_copy.json"
        )

        shutil.copy(self.scrollbar_settings_file, self.scrollbar_settings_temp_file)

        self.system_helper.SCROLLBAR_SETTINGS_PATH = self.scrollbar_settings_temp_file

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_default_settings(self):
        actual = self.system_helper.is_scrollbar_enabled()
        self.assertFalse(actual)

    def test_toggle_scrollbar_enabled(self):
        actual = self.system_helper.is_scrollbar_enabled()
        self.assertFalse(actual)

        self.system_helper.toggle_scrollbar_enabled()
        actual = self.system_helper.is_scrollbar_enabled()
        self.assertTrue(actual)

        self.system_helper.toggle_scrollbar_enabled()
        actual = self.system_helper.is_scrollbar_enabled()
        self.assertFalse(actual)
