import os
import unittest
from unittest.mock import patch

from helper.Constants import Constants


class TestConstants(unittest.TestCase):
    def setUp(self):
        os.environ["RETROI_DIR"] = "/home/pi/Retro.I"
        self.constants = Constants()

    def tearDown(self):
        os.environ.pop("RETROI_DIR", None)

    def test_pwd(self):
        self.assertEqual("/home/pi/Retro.I", Constants.pwd())

    def test_sound_path(self):
        self.assertEqual(
            "/home/pi/Retro.I/assets/sounds", self.constants.sound_path()
        )

    def test_toast_path(self):
        self.assertEqual(
            "/home/pi/Retro.I/assets/toasts", self.constants.toast_path()
        )

    def test_button_img(self):
        os.environ["RETROI_DIR"] = "."  # overwrite for testing
        self.assertIn("/assets/buttons", self.constants.get_button_img())

    def test_default_current_radio_station(self):
        self.assertEqual({}, self.constants.current_radio_station)

    def test_default_indicator_refs(self):
        self.assertEqual([], self.constants.indicator_refs)

    @patch("helper.Constants.subprocess.check_output")
    def test_service_start_time(self, mock_time):
        mock_time.return_value = (
            "ActiveEnterTimestamp=Wed 2026-01-14 20:00:00 CET"
        )

        actual = Constants.get_service_start_time()

        mock_time.assert_any_call(
            ["systemctl", "show", "retroi", "-p", "ActiveEnterTimestamp"],
            text=True,
        )

        expected = "2026-01-14 20:00:00"
        self.assertEqual(f"{actual}", expected)
