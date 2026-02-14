from core.settings.base.scrollbar_settings import BaseScrollbarSettings


class WebScrollbarSettings(BaseScrollbarSettings):
    def is_scrollbar_enabled(self) -> bool:
        return False

    def toggle_scrollbar_enabled(self):
        pass
