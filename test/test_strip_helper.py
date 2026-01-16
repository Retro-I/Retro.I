from helper.Constants import Constants
from test.base_test import BaseTest

constants = Constants()


class TestStripSettingsHelper(BaseTest):
    def setUp(self):
        super().setUp()

    def test_is_strip_active(self):
        actual = self.strip_settings_helper.is_strip_active()
        self.assertTrue(actual)

        self.strip_settings_helper.update_settings(is_active=False)
        actual = self.strip_settings_helper.is_strip_active()
        self.assertFalse(actual)

        self.strip_settings_helper.update_settings(is_active=True)
        actual = self.strip_settings_helper.is_strip_active()
        self.assertTrue(actual)

    def test_get_led_length(self):
        actual = self.strip_settings_helper.get_led_length()
        self.assertEqual(actual, 38)

    def test_get_curr_brightness(self):
        actual = self.strip_settings_helper.get_curr_brightness()
        self.assertEqual(actual, 100)

    def test_update_curr_brightness(self):
        actual = self.strip_settings_helper.get_curr_brightness()
        self.assertEqual(actual, 100)

        self.strip_settings_helper.update_settings(brightness=12.3)
        actual = self.strip_settings_helper.get_curr_brightness()
        self.assertEqual(actual, 12.3)

    def test_get_complete_settings(self):
        actual = self.strip_settings_helper.get_strip_settings()
        expected = {
            "isStripEnabled": True,
            "brightness": 100.0,
            "amountLeds": 38,
        }
        self.assertCountEqual(actual, expected)
