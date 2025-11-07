import json

import flet as ft

from helper.Constants import Constants

c = Constants()


class ThemeHelper:
    THEME_SETTINGS_PATH = f"{c.settings_path()}/theme-mode-settings.json"

    def load_theme_settings(self) -> dict:
        with open(self.THEME_SETTINGS_PATH) as file:
            data = json.load(file)
            return data

    def get_theme(self) -> ft.ThemeMode:
        theme = self.load_theme_settings()["theme"]
        if theme == "light":
            return ft.ThemeMode.LIGHT
        elif theme == "dark":
            return ft.ThemeMode.DARK
        else:
            return ft.ThemeMode.SYSTEM

    def toggle_theme(self):
        settings = self.load_theme_settings()
        theme = self.get_theme()

        settings["theme"] = "light" if theme == ft.ThemeMode.DARK else "dark"

        with open(self.THEME_SETTINGS_PATH, "r+") as file:
            file.seek(0)
            json.dump(settings, file, indent=4)
            file.truncate()
