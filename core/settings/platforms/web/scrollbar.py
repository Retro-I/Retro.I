from core.settings.base.scrollbar import BaseScrollbarSettings


class WebScrollbarSettings(BaseScrollbarSettings):
    def is_scrollbar_enabled(self) -> bool:
        return False

    def toggle_scrollbar_enabled(self):
        pass
