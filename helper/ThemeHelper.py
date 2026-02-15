import json

import flet as ft

from core.helpers.factories.settings_sync import create_settings_sync_helper
from helper.Constants import Constants

c = Constants()


class ThemeHelper:
    SETTING = "theme-mode-settings.json"
    THEME_SETTINGS_PATH = f"{Constants.settings_path()}/{SETTING}"

    def __init__(self):
        self.settings_sync_helper = create_settings_sync_helper()

    def _load_theme_settings(self) -> dict:
        def _get_data():
            with open(self.THEME_SETTINGS_PATH) as file:
                data = json.load(file)
                return data

        try:
            return _get_data()
        except Exception:
            self.settings_sync_helper.reset_settings_file(self.SETTING)
            return _get_data()

    def get_theme(self) -> ft.ThemeMode:
        theme = self._load_theme_settings()["theme"]
        if theme == "light":
            return ft.ThemeMode.LIGHT
        elif theme == "dark":
            return ft.ThemeMode.DARK
        else:
            return ft.ThemeMode.SYSTEM

    def toggle_theme(self):
        settings = self._load_theme_settings()
        theme = self.get_theme()

        settings["theme"] = "light" if theme == ft.ThemeMode.DARK else "dark"

        with open(self.THEME_SETTINGS_PATH, "r+") as file:
            file.seek(0)
            json.dump(settings, file, indent=4)
            file.truncate()
