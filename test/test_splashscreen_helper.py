from helper.Constants import Constants
from test.base_test import BaseTest

constants = Constants()


class TestSplashscreenHelper(BaseTest):
    def test_get_splashscreens(self):
        actual = self.splashscreen_helper.get_splashscreens()
        expected = ["splash.png", "splash_1.png", "splash_2.png", "splash_3.png", "splash_4.png"]

        self.assertEqual(actual, expected)
