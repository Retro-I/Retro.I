from helper.Constants import Constants
from test.base_test import BaseTest

constants = Constants()


class TestGpioHelper(BaseTest):
    def setUp(self):
        super().setUp()

    def test_default_mappings(self):
        actual = self.gpio_helper.get_mappings()
        expected = {
            "ROTARY_VOLUME_UP": "6",
            "ROTARY_VOLUME_DOWN": "12",
            "ROTARY_VOLUME_PRESS": "13",
            "ROTARY_BASS_UP": "4",
            "ROTARY_BASS_DOWN": "14",
            "ROTARY_PITCH_UP": "11",
            "ROTARY_PITCH_DOWN": "8",
            "START_PARTY_MODE_BUTTON": "21",
        }
        self.assertCountEqual(actual, expected)
