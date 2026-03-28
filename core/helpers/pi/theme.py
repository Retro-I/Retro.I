from core.helpers.base.theme import BaseThemeHelper
from helper.theme_helper import ThemeHelper


class PiThemeHelper(BaseThemeHelper):
    def __init__(self):
        self.helper = ThemeHelper()

    def get_theme(self):
        return self.helper.get_theme()

    def toggle_theme(self):
        self.helper.toggle_theme()
