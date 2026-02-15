import os
import unittest

from core.app_platform import AppPlatform, get_app_platform


class TestAppPlatform(unittest.TestCase):
    def test_pi_app_platform(self):
        os.environ["APP_PLATFORM"] = "PI"
        actual = get_app_platform()
        expected = AppPlatform.PI
        self.assertEqual(actual, expected)

    def test_web_app_platform(self):
        os.environ["APP_PLATFORM"] = "WEB"
        actual = get_app_platform()
        expected = AppPlatform.WEB
        self.assertEqual(actual, expected)

    def test_default_app_platform(self):
        actual = get_app_platform()
        expected = AppPlatform.PI
        self.assertEqual(actual, expected)
