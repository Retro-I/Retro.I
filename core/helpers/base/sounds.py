class BaseSoundsHelper:
    def search_sounds(self, query):
        raise NotImplementedError

    def add_favorite_sound(self, item):
        raise NotImplementedError

    def delete_favorite_sound(self, item):
        raise NotImplementedError

    def load_favorite_sounds(self):
        raise NotImplementedError

    def load_toasts(self):
        raise NotImplementedError

    def get_random_toast(self):
        raise NotImplementedError
