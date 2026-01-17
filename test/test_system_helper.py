import os
import sys
import unittest
from unittest import mock
from unittest.mock import MagicMock, patch

from freezegun import freeze_time

from test.helper.mock_netifaces import (
    mock_lan_netifaces,
    mock_none_netifaces,
    mock_wifi_netifaces,
)


class TestSystemHelper(unittest.TestCase):
    @patch.dict(sys.modules, {"alsaaudio": MagicMock()})
    @patch.dict(sys.modules, {"vlc": MagicMock()})
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

        from helper.SystemHelper import SystemHelper

        self.system_helper = SystemHelper()

    def tearDown(self):
        os.environ["PARTY_MODE"] = "0"

    @patch("socket.gethostname")
    def test_get_hostname(self, mock_hostname):
        mock_hostname.return_value = "hostname"

        actual = self.system_helper.get_hostname()
        self.assertEqual(actual, "hostname")

    @mock.patch("os.system")
    @mock.patch("time.sleep")
    def test_shutdown_system(self, mock_sleep, mock_os_system_call):
        self.system_helper.shutdown_system()
        mock_sleep.assert_called_once_with(3)
        mock_os_system_call.assert_called_once_with("sudo shutdown -h 0")

    @mock.patch("os.system")
    @mock.patch("time.sleep")
    def test_restart_system(self, mock_sleep, mock_os_system_call):
        self.system_helper.restart_system()
        mock_sleep.assert_called_once_with(3)
        mock_os_system_call.assert_called_once_with("sudo reboot")

    @mock.patch("os.system")
    def test_stop_app(self, mock_os_system_call):
        self.system_helper.stop_app()
        mock_os_system_call.assert_called_once_with(
            "sudo systemctl stop retroi"
        )

    @mock.patch("os.system")
    def test_restart_app(self, mock_os_system_call):
        self.system_helper.restart_app()
        mock_os_system_call.assert_called_once_with(
            "sudo systemctl restart retroi"
        )

    @freeze_time("2026-01-14 20:00:00")
    def test_get_curr_date(self):
        actual = self.system_helper.get_curr_date()
        expected = "14.01.2026"
        self.assertEqual(actual, expected)

    def test_init_party_mode(self):
        self.system_helper.init_party_mode()
        self.assertEqual(self.system_helper.is_party, "0")

        os.environ["PARTY_MODE"] = "1"

        self.system_helper.init_party_mode()
        self.assertEqual(self.system_helper.is_party, "1")

    def test_is_party_mode(self):
        self.assertFalse(self.system_helper.is_party_mode())
        self.system_helper.init_party_mode()
        self.assertFalse(self.system_helper.is_party_mode())
        os.environ["PARTY_MODE"] = "1"
        self.assertFalse(self.system_helper.is_party_mode())
        self.system_helper.init_party_mode()
        self.assertTrue(self.system_helper.is_party_mode())
        os.environ["PARTY_MODE"] = "0"
        self.assertTrue(self.system_helper.is_party_mode())
        self.system_helper.init_party_mode()
        self.assertFalse(self.system_helper.is_party_mode())

    def test_image_path_remote(self):
        actual = self.system_helper.get_img_path(
            "https://test.test.de/image.png"
        )
        expected = "https://test.test.de/image.png"
        self.assertEqual(actual, expected)

    def test_image_path_local(self):
        actual = self.system_helper.get_img_path("test.png")
        expected = "assets/stations/test.png"
        self.assertTrue(expected in actual)

    @unittest.skip
    def test_change_curr_brightness(self):
        pass

    def test_get_curr_brightness(self):
        actual = self.system_helper.get_curr_brightness()
        expected_mocked = 100
        self.assertEqual(actual, expected_mocked)


class TestSystemHelperWifiNetwork(unittest.TestCase):
    @patch.dict(sys.modules, {"alsaaudio": MagicMock()})
    @patch.dict(sys.modules, {"vlc": MagicMock()})
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

        from helper.SystemHelper import SystemHelper

        self.system_helper = SystemHelper()

    @patch("netifaces.gateways")
    @patch("netifaces.ifaddresses")
    def test_default_interface_wifi(self, mock_ifaddresses, mock_gateways):
        mock_wifi_netifaces(mock_gateways, mock_ifaddresses)

        actual = self.system_helper.get_default_interface()
        self.assertEqual(actual, "wlan0")

    @patch("netifaces.gateways")
    @patch("netifaces.ifaddresses")
    @patch("subprocess.run")
    def test_get_current_ssid_wifi(
        self, ssid_mock, mock_ifaddresses, mock_gateways
    ):
        mock_wifi_netifaces(mock_gateways, mock_ifaddresses)

        ssid_mock.return_value = MagicMock(stdout=b"\rWIFI_SSID   \n")

        actual = self.system_helper.get_current_ssid()
        self.assertEqual(actual, "WIFI_SSID")

        @patch("netifaces.gateways")
        @patch("netifaces.ifaddresses")
        @patch("subprocess.run")
        def test_get_current_ssid_wifi(
            self, ssid_mock, mock_ifaddresses, mock_gateways
        ):
            mock_wifi_netifaces(mock_gateways, mock_ifaddresses)

            ssid_mock.return_value = MagicMock(stdout=b"\rWIFI_SSID   \n")

            actual = self.system_helper.get_current_ssid()
            self.assertEqual(actual, "WIFI_SSID")

    @patch("netifaces.gateways")
    @patch("netifaces.ifaddresses")
    def test_get_ip_address_wifi(self, mock_ifaddresses, mock_gateways):
        mock_wifi_netifaces(mock_gateways, mock_ifaddresses)

        actual = self.system_helper.get_ip_address()
        self.assertEqual(actual, "192.168.2.106")

    @patch("netifaces.gateways")
    @patch("netifaces.ifaddresses")
    def test_get_netmask_wifi(self, mock_ifaddresses, mock_gateways):
        mock_wifi_netifaces(mock_gateways, mock_ifaddresses)

        actual = self.system_helper.get_netmask()
        self.assertEqual(actual, "255.255.255.0")

    @patch("netifaces.gateways")
    @patch("netifaces.ifaddresses")
    def test_get_mac_address_wifi(self, mock_ifaddresses, mock_gateways):
        mock_wifi_netifaces(mock_gateways, mock_ifaddresses)

        actual = self.system_helper.get_mac_address()
        self.assertEqual(actual, "XX:XX:XX:XX:XX:XX")


class TestSystemHelperLanNetwork(unittest.TestCase):
    @patch.dict(sys.modules, {"alsaaudio": MagicMock()})
    @patch.dict(sys.modules, {"vlc": MagicMock()})
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

        from helper.SystemHelper import SystemHelper

        self.system_helper = SystemHelper()

    @patch("netifaces.gateways")
    @patch("netifaces.ifaddresses")
    def test_default_interface_lan(self, mock_ifaddresses, mock_gateways):
        mock_lan_netifaces(mock_gateways, mock_ifaddresses)

        actual = self.system_helper.get_default_interface()
        self.assertEqual(actual, "eth0")

    @patch("netifaces.gateways")
    @patch("netifaces.ifaddresses")
    @patch("subprocess.run")
    def test_get_current_ssid_lan(
        self, ssid_mock, mock_ifaddresses, mock_gateways
    ):
        mock_lan_netifaces(mock_gateways, mock_ifaddresses)

        ssid_mock.return_value = MagicMock(stdout=b"\rWIFI_SSID   \n")

        actual = self.system_helper.get_current_ssid()
        self.assertEqual(actual, "")

    @patch("netifaces.gateways")
    @patch("netifaces.ifaddresses")
    def test_get_ip_address_lan(self, mock_ifaddresses, mock_gateways):
        mock_lan_netifaces(mock_gateways, mock_ifaddresses)

        actual = self.system_helper.get_ip_address()
        self.assertEqual(actual, "192.168.2.100")

    @patch("netifaces.gateways")
    @patch("netifaces.ifaddresses")
    def test_get_netmask_lan(self, mock_ifaddresses, mock_gateways):
        mock_lan_netifaces(mock_gateways, mock_ifaddresses)

        actual = self.system_helper.get_netmask()
        self.assertEqual(actual, "255.255.0.0")

    @patch("netifaces.gateways")
    @patch("netifaces.ifaddresses")
    def test_get_mac_address_lan(self, mock_ifaddresses, mock_gateways):
        mock_lan_netifaces(mock_gateways, mock_ifaddresses)

        actual = self.system_helper.get_mac_address()
        self.assertEqual(actual, "AB:DE:EF:GH:IJ:KL")


class TestSystemHelperNoneNetwork(unittest.TestCase):
    @patch.dict(sys.modules, {"alsaaudio": MagicMock()})
    @patch.dict(sys.modules, {"vlc": MagicMock()})
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

        from helper.SystemHelper import SystemHelper

        self.system_helper = SystemHelper()

    @patch("netifaces.gateways")
    @patch("netifaces.ifaddresses")
    def test_default_interface_none(self, mock_ifaddresses, mock_gateways):
        mock_none_netifaces(mock_gateways, mock_ifaddresses)

        actual = self.system_helper.get_default_interface()
        self.assertEqual(actual, None)

    @patch("netifaces.gateways")
    @patch("netifaces.ifaddresses")
    @patch("subprocess.run")
    def test_get_current_ssid_none(
        self, ssid_mock, mock_ifaddresses, mock_gateways
    ):
        mock_none_netifaces(mock_gateways, mock_ifaddresses)

        ssid_mock.return_value = MagicMock(stdout=b"")

        actual = self.system_helper.get_current_ssid()
        self.assertEqual(actual, "")

    @patch("netifaces.gateways")
    @patch("netifaces.ifaddresses")
    def test_get_ip_address_none(self, mock_ifaddresses, mock_gateways):
        mock_none_netifaces(mock_gateways, mock_ifaddresses)

        actual = self.system_helper.get_ip_address()
        self.assertEqual(actual, "")

    @patch("netifaces.gateways")
    @patch("netifaces.ifaddresses")
    def test_get_netmask_none(self, mock_ifaddresses, mock_gateways):
        mock_none_netifaces(mock_gateways, mock_ifaddresses)

        actual = self.system_helper.get_netmask()
        self.assertEqual(actual, "")

    @patch("netifaces.gateways")
    @patch("netifaces.ifaddresses")
    def test_get_mac_address_none(self, mock_ifaddresses, mock_gateways):
        mock_none_netifaces(mock_gateways, mock_ifaddresses)

        actual = self.system_helper.get_mac_address()
        self.assertEqual(actual, "")

    @patch("netifaces.gateways")
    @patch("netifaces.ifaddresses")
    def test_get_network_config_none(self, mock_ifaddresses, mock_gateways):
        mock_none_netifaces(mock_gateways, mock_ifaddresses)

        actual = self.system_helper.get_network_config()
        expected = {
            "ssid": "",
            "ip": "",
            "hostname": "",
            "subnetmask": "",
            "mac_address": "",
            "gateway": "",
            "dns": ["", ""],
        }
        self.assertEqual(actual, expected)
