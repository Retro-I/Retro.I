import sys
import unittest
from unittest.mock import MagicMock, patch


class TestStripSettingsHelper(unittest.TestCase):
    @patch.dict(sys.modules, {"alsaaudio": MagicMock()})
    @patch.dict(sys.modules, {"playsound3": MagicMock()})
    @patch.dict(sys.modules, {"cairosvg": MagicMock()})
    @patch.dict(sys.modules, {"numpy": MagicMock()})
    @patch.dict(sys.modules, {"joblib": MagicMock()})
    @patch.dict(sys.modules, {"sklearn.cluster": MagicMock()})
    @patch.dict(sys.modules, {"board": MagicMock()})
    @patch.dict(sys.modules, {"neopixel": MagicMock()})
    @patch.dict(sys.modules, {"adafruit_led_animation": MagicMock()})
    @patch.dict(sys.modules, {"adafruit_led_animation.color": MagicMock()})
    @patch.dict(
        sys.modules, {"adafruit_led_animation.animation.pulse": MagicMock()}
    )
    @patch("helper.StripSettingsHelper.StripSettingsHelper.get_strip_settings")
    def setUp(self, get_strip_settings):
        get_strip_settings.return_value = {
            "amountLeds": 38,
            "brightness": 100,
            "isStripEnabled": True,
        }
        super().setUp()

        from helper.LogsHelper import LogsHelper

        self.logs_helper = LogsHelper()

    @patch("helper.LogsHelper.subprocess.check_output")
    @patch("helper.Constants.Constants.get_service_start_time")
    def test_logs(self, mock_time, mock_get_logs):
        mock_time.return_value = "2026-01-14 20:00:00"
        mock_get_logs.return_value = "some_nice_logs\nmore_logs\neven_more_logs"

        actual = self.logs_helper.get_logs()
        expected = "some_nice_logs\nmore_logs\neven_more_logs"
        self.assertEqual(actual, expected)

        mock_get_logs.assert_any_call(
            [
                "journalctl",
                "-u",
                "retroi",
                "-S",
                "2026-01-14 20:00:00",
                "--no-pager",
            ],
            text=True,
        )
