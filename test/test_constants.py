import os
import unittest

from helper.Constants import Constants


class TestConstants(unittest.TestCase):
    def setUp(self):
        os.environ["RETROI_DIR"] = "/home/pi/Retro.I"
        self.constants = Constants()

    def test_pwd(self):
        self.assertEqual("/home/pi/Retro.I", self.constants.pwd())

    def test_sound_path(self):
        self.assertEqual("/home/pi/Retro.I/assets/sounds", self.constants.sound_path())

    def test_toast_path(self):
        self.assertEqual("/home/pi/Retro.I/assets/toasts", self.constants.toast_path())

    def test_button_img(self):
        os.environ["RETROI_DIR"] = "."  # overwrite for testing
        self.assertIn("/assets/buttons", self.constants.get_button_img())

    def test_default_current_radio_station(self):
        self.assertEqual({}, self.constants.current_radio_station)

    def test_default_current_station_index_to_delete(self):
        self.assertEqual(None, self.constants.current_station_index_to_delete)

    def test_default_indicator_refs(self):
        self.assertEqual([], self.constants.indicator_refs)
