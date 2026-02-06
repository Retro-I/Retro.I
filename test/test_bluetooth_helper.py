import sys
import unittest
from unittest.mock import MagicMock, patch

from helper.Constants import Constants

constants = Constants()


class TestBluetoothHelper(unittest.TestCase):
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
    def setUp(self, _):
        from helper.BluetoothHelper import BluetoothHelper

        self.bluetooth_helper = BluetoothHelper()

    @patch("helper.BluetoothHelper.subprocess.check_output")
    def test_get_paired_devices(self, mock_get_paired_devices):
        mock_get_paired_devices.return_value = "Device FF:FF:FF:FF:FF:FF Device_Name\nDevice FF:FF:FF:FF:FF:AB Device_Name2"

        actual = self.bluetooth_helper.get_paired_devices()
        expected = [
            {
                "name": "Device_Name",
                "mac_address": "FF:FF:FF:FF:FF:FF",
            },
            {
                "name": "Device_Name2",
                "mac_address": "FF:FF:FF:FF:FF:AB",
            },
        ]
        self.assertEqual(actual, expected)

        mock_get_paired_devices.assert_any_call(
            ["bluetoothctl", "devices", "Paired"], text=True
        )

    @patch("helper.BluetoothHelper.subprocess.check_output")
    def test_get_paired_devices_filter_duplicates(
        self, mock_get_paired_devices
    ):
        mock_get_paired_devices.return_value = "Device FF:FF:FF:FF:FF:FF Device_Name\nDevice FF:FF:FF:FF:FF:FF Device_Name"

        actual = self.bluetooth_helper.get_paired_devices()
        expected = [
            {
                "name": "Device_Name",
                "mac_address": "FF:FF:FF:FF:FF:FF",
            }
        ]
        self.assertEqual(actual, expected)

        mock_get_paired_devices.assert_any_call(
            ["bluetoothctl", "devices", "Paired"], text=True
        )

    @patch("helper.BluetoothHelper.subprocess.check_output")
    def test_get_paired_devices_empty_list(self, mock_get_paired_devices):
        mock_get_paired_devices.return_value = (
            "Device XX:XX:XX:XX:XX:XX Device_Name"
        )

        actual = self.bluetooth_helper.get_paired_devices()
        expected = []
        self.assertEqual(actual, expected)

        mock_get_paired_devices.assert_any_call(
            ["bluetoothctl", "devices", "Paired"], text=True
        )
