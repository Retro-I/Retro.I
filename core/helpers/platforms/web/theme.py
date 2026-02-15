import flet as ft

from core.helpers.base.theme import BaseThemeHelper


class WebThemeHelper(BaseThemeHelper):
    def get_theme(self):
        return ft.ThemeMode.SYSTEM

    def toggle_theme(self):
        pass
