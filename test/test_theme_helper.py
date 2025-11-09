from test.base_test import BaseTest

import flet as ft

from helper.Constants import Constants

constants = Constants()


class TestThemeHelper(BaseTest):
    def setUp(self):
        super().setUp()

    def test_get_theme(self):
        actual = self.theme_helper.get_theme()
        self.assertEqual(actual, ft.ThemeMode.LIGHT)

    def test_toggle_theme(self):
        actual = self.theme_helper.get_theme()
        self.assertEqual(actual, ft.ThemeMode.LIGHT)

        self.theme_helper.toggle_theme()
        actual = self.theme_helper.get_theme()
        self.assertEqual(actual, ft.ThemeMode.DARK)

        self.theme_helper.toggle_theme()
        actual = self.theme_helper.get_theme()
        self.assertEqual(actual, ft.ThemeMode.LIGHT)
