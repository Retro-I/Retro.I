from core.helpers.base.sounds import BaseSoundsHelper


class WebSoundsHelper(BaseSoundsHelper):
    def search_sounds(self, query):
        return []

    def add_favorite_sound(self, item):
        pass

    def delete_favorite_sound(self, item):
        pass

    def load_favorite_sounds(self):
        return []

    def load_toasts(self):
        return []

    def get_random_toast(self):
        return {}
