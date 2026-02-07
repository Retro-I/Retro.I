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

    def test_is_static_color(self):
        self.assertFalse(self.strip_settings_helper.is_static_color())

    def test_get_static_color(self):
        actual = self.strip_settings_helper.get_static_color()
        self.assertEqual(actual, "#6A540C")

    def test_update_curr_brightness(self):
        actual = self.strip_settings_helper.get_curr_brightness()
        self.assertEqual(actual, 100)

        self.strip_settings_helper.update_settings(brightness=12.3)
        actual = self.strip_settings_helper.get_curr_brightness()
        self.assertEqual(actual, 12.3)

    def test_update_is_static_color(self):
        self.strip_settings_helper.update_settings(is_static_color=True)
        self.assertTrue(self.strip_settings_helper.is_static_color())

        self.strip_settings_helper.update_settings(is_static_color=False)
        self.assertFalse(self.strip_settings_helper.is_static_color())

    def test_update_static_color(self):
        self.strip_settings_helper.update_settings(static_color="#000000")
        actual = self.strip_settings_helper.get_static_color()
        self.assertEqual(actual, "#000000")

    def test_update_static_color_letter(self):
        self.strip_settings_helper.update_settings(static_color="#FFFFFF")
        actual = self.strip_settings_helper.get_static_color()
        self.assertEqual(actual, "#FFFFFF")

    def test_update_static_color_lower_case(self):
        self.strip_settings_helper.update_settings(static_color="#ddeeff")
        actual = self.strip_settings_helper.get_static_color()
        self.assertEqual(actual, "#DDEEFF")

    def test_update_static_color_not_valid(self):
        self.strip_settings_helper.update_settings(static_color="#XXYYZZ")
        actual = self.strip_settings_helper.get_static_color()
        self.assertEqual(actual, "#6A540C")

    def test_update_static_color_invalid_length(self):
        self.strip_settings_helper.update_settings(static_color="#ABCDEFABCDEF")
        actual = self.strip_settings_helper.get_static_color()
        self.assertEqual(actual, "#6A540C")

    def test_get_complete_settings(self):
        actual = self.strip_settings_helper.get_strip_settings()
        expected = {
            "isStripEnabled": True,
            "brightness": 100.0,
            "amountLeds": 38,
            "isStaticColor": False,
            "staticColor": "#6A540C",
        }
        self.assertCountEqual(actual, expected)
