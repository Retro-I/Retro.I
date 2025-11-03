import os
import unittest

from helper.Constants import Constants


class TestConstants(unittest.TestCase):
    def setUp(self):
        self.constants = Constants()

    def test_pwd(self):
        os.environ["RETROI_DIR"] = "/home/pi/Retro.I"
        self.assertEquals("/home/pi/Retro.I", self.constants.pwd())
