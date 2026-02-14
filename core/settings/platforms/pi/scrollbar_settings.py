from core.settings.base.scrollbar_settings import BaseScrollbarSettings
from helper.ScrollbarSettingsHelper import ScrollbarSettingsHelper


class PiScrollbarSettings(BaseScrollbarSettings):
    def __init__(self):
        self.settings = ScrollbarSettingsHelper()

    def is_scrollbar_enabled(self) -> bool:
        return self.settings.is_scrollbar_enabled()

    def toggle_scrollbar_enabled(self):
        self.settings.toggle_scrollbar_enabled()
