class BaseScrollbarSettings:
    def is_scrollbar_enabled(self) -> bool:
        raise NotImplementedError

    def toggle_scrollbar_enabled(self):
        raise NotImplementedError
