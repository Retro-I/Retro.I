import subprocess
import sys
import unittest
from unittest.mock import MagicMock, patch

from helper.Constants import Constants

constants = Constants()


strip_mock = {
    "isStripEnabled": True,
    "brightness": 100.0,
    "amountLeds": 38,
    "isStaticColor": False,
    "staticColor": "#6A540C",
}


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
    def setUp(self, get_strip_settings):
        get_strip_settings.return_value = strip_mock

        from helper.BluetoothHelper import BluetoothHelper

        self.bluetooth_helper = BluetoothHelper()

    @patch("os.system")
    def test_turn_on(self, mock):
        self.bluetooth_helper.turn_on()
        mock.assert_called_once_with("rfkill unblock 0")

    @patch("helper.BluetoothHelper.subprocess.run")
    def test_turn_off(self, mock):
        self.bluetooth_helper.turn_off()
        mock.assert_any_call(
            ["rfkill", "block", "0"], stdout=subprocess.DEVNULL
        )

    @patch("helper.BluetoothHelper.subprocess.run")
    def test_is_bluetooth_on(self, mock):
        mock.return_value = MagicMock(
            stdout=b"""hci0:   Type: Primary  Bus: UART
                   BD Address: D8:3A:DD:22:B0:45  ACL MTU: 1021:8  SCO MTU: 64:1
                   RUNNING
                   RX bytes:9638860 acl:28574 sco:0 events:740 errors:0
                   TX bytes:76395 acl:233 sco:0 commands:579 errors:0
            """
        )
        self.assertTrue(self.bluetooth_helper.is_bluetooth_on())
        mock.assert_any_call(["hciconfig"], stdout=subprocess.PIPE)

    @patch("helper.BluetoothHelper.subprocess.run")
    def test_is_bluetooth_off(self, mock):
        mock.return_value = MagicMock(
            stdout=b"""hci0:   Type: Primary  Bus: UART
                   BD Address: D8:3A:DD:22:B0:45  ACL MTU: 1021:8  SCO MTU: 64:1
                   DOWN
                   RX bytes:9638860 acl:28574 sco:0 events:740 errors:0
                   TX bytes:76395 acl:233 sco:0 commands:579 errors:0
            """
        )
        self.assertFalse(self.bluetooth_helper.is_bluetooth_on())
        mock.assert_any_call(["hciconfig"], stdout=subprocess.PIPE)

    @patch("os.system")
    def test_discovery_on(self, mock):
        self.bluetooth_helper.bluetooth_discovery_on()
        mock.assert_any_call("bluetoothctl discoverable on")
        self.assertTrue(self.bluetooth_helper.discovery_on)

    @patch("os.system")
    def test_discovery_off(self, mock):
        self.bluetooth_helper.bluetooth_discovery_off()
        mock.assert_any_call("bluetoothctl discoverable off")
        self.assertFalse(self.bluetooth_helper.discovery_on)

    @patch("helper.BluetoothHelper.subprocess.run")
    def test_get_bluetooth_display_name(self, mock):
        mock.return_value = MagicMock(stdout=" Test-Name")
        actual = self.bluetooth_helper.get_bluetooth_display_name()
        expected = "Test-Name"
        self.assertEqual(actual, expected)

        mock.assert_any_call(
            'bluetoothctl show | grep "Alias:" | cut -d ":" -f2-',
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True,
        )

    @patch("helper.BluetoothHelper.BluetoothHelper.turn_off")
    @patch("helper.BluetoothHelper.BluetoothHelper.turn_on")
    @patch("os.system")
    def test_change_bluetooth_display_name(
        self, mock_system, mock_turn_on, mock_turn_off
    ):
        mock_system.return_value = MagicMock()
        self.bluetooth_helper.change_bluetooth_display_name("Test-Name")
        mock_turn_off.assert_called_once()
        mock_system.assert_any_call('bluetoothctl system-alias "Test-Name"')
        mock_turn_on.assert_called_once()

    @patch("helper.BluetoothHelper.subprocess.run")
    def test_connect(self, mock_system):
        mock_system.return_value = MagicMock()
        self.bluetooth_helper.connect("AA:AA:AA:AA:AA:AA")
        mock_system.assert_any_call(
            ["bluetoothctl", "connect", "AA:AA:AA:AA:AA:AA"]
        )

    @patch("helper.BluetoothHelper.subprocess.run")
    def test_disconnect(self, mock_system):
        mock_system.return_value = MagicMock()
        self.bluetooth_helper.disconnect("AA:AA:AA:AA:AA:AA")
        mock_system.assert_any_call(
            ["bluetoothctl", "disconnect", "AA:AA:AA:AA:AA:AA"]
        )

    @patch("helper.BluetoothHelper.subprocess.run")
    @patch("helper.BluetoothHelper.BluetoothHelper.get_connected_device_mac")
    def test_disconnect_with_connected_device(
        self, mock_connected_mac, mock_system
    ):
        mock_connected_mac.return_value = "BB:BB:BB:BB:BB:BB"
        mock_system.return_value = MagicMock()
        self.bluetooth_helper.disconnect()
        mock_system.assert_any_call(
            ["bluetoothctl", "disconnect", "BB:BB:BB:BB:BB:BB"]
        )

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

    @patch("helper.BluetoothHelper.subprocess.run")
    def test_remove_device(self, mock_system):
        mock_system.return_value = MagicMock()
        self.bluetooth_helper.remove_device("AA:AA:AA:AA:AA:AA")
        mock_system.assert_any_call(
            ["bluetoothctl", "remove", "AA:AA:AA:AA:AA:AA"]
        )

    @patch("helper.BluetoothHelper.subprocess.run")
    def test_get_connected_device(self, mock_system):
        mock_system.return_value = MagicMock(
            stdout=b"Device AA:AA:AA:AA:AA:AA Test-Name"
        )
        actual = self.bluetooth_helper.get_connected_device()
        expected = "Device AA:AA:AA:AA:AA:AA Test-Name"
        self.assertEqual(actual, expected)
        mock_system.assert_any_call(
            ["bluetoothctl", "devices", "Connected"],
            stdout=subprocess.PIPE,
        )

    @patch("helper.BluetoothHelper.subprocess.run")
    def test_get_connected_device_empty(self, mock_system):
        mock_system.return_value = MagicMock(stdout=b"")
        actual = self.bluetooth_helper.get_connected_device()
        expected = ""
        self.assertEqual(actual, expected)
        mock_system.assert_any_call(
            ["bluetoothctl", "devices", "Connected"],
            stdout=subprocess.PIPE,
        )

    @patch("helper.BluetoothHelper.subprocess.run")
    def test_get_connected_device_name(self, mock_system):
        mock_system.return_value = MagicMock(
            stdout=b"Device AA:AA:AA:AA:AA:AA Test-Name"
        )
        actual = self.bluetooth_helper.get_connected_device_name()
        expected = "Test-Name"
        self.assertEqual(actual, expected)
        mock_system.assert_any_call(
            ["bluetoothctl", "devices", "Connected"],
            stdout=subprocess.PIPE,
        )

    @patch("helper.BluetoothHelper.subprocess.run")
    def test_get_connected_device_name_empty(self, mock_system):
        mock_system.return_value = MagicMock(stdout=b"")
        actual = self.bluetooth_helper.get_connected_device_name()
        expected = ""
        self.assertEqual(actual, expected)
        mock_system.assert_any_call(
            ["bluetoothctl", "devices", "Connected"],
            stdout=subprocess.PIPE,
        )

    @patch("helper.BluetoothHelper.subprocess.run")
    def test_get_connected_device_mac(self, mock_system):
        mock_system.return_value = MagicMock(
            stdout=b"Device AA:AA:AA:AA:AA:AA Test-Name"
        )
        actual = self.bluetooth_helper.get_connected_device_mac()
        expected = "AA:AA:AA:AA:AA:AA"
        self.assertEqual(actual, expected)
        mock_system.assert_any_call(
            ["bluetoothctl", "devices", "Connected"],
            stdout=subprocess.PIPE,
        )

    @patch("helper.BluetoothHelper.subprocess.run")
    def test_get_connected_device_mac_empty(self, mock_system):
        mock_system.return_value = MagicMock(stdout=b"")
        actual = self.bluetooth_helper.get_connected_device_mac()
        expected = ""
        self.assertEqual(actual, expected)
        mock_system.assert_any_call(
            ["bluetoothctl", "devices", "Connected"],
            stdout=subprocess.PIPE,
        )

    @patch("helper.BluetoothHelper.subprocess.run")
    def test_is_connected(self, mock_system):
        mock_system.return_value = MagicMock(
            stdout=b"Device AA:AA:AA:AA:AA:AA Test-Name"
        )
        self.assertTrue(self.bluetooth_helper.is_connected())
        mock_system.assert_any_call(
            ["bluetoothctl", "devices", "Connected"],
            stdout=subprocess.PIPE,
        )

    @patch("helper.BluetoothHelper.subprocess.run")
    def test_is_not_connected(self, mock_system):
        mock_system.return_value = MagicMock(stdout=b"")
        self.assertFalse(self.bluetooth_helper.is_connected())
        mock_system.assert_any_call(
            ["bluetoothctl", "devices", "Connected"],
            stdout=subprocess.PIPE,
        )
