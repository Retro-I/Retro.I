from core.helpers.base.sounds import BaseSoundsHelper
from helper.Sounds import Sounds


class PiSoundsHelper(BaseSoundsHelper):
    def __init__(self):
        self.helper = Sounds()

    def search_sounds(self, query):
        return self.helper.search_sounds(query)

    def add_favorite_sound(self, item):
        self.helper.add_favorite_sound(item)

    def delete_favorite_sound(self, item):
        self.helper.delete_favorite_sound(item)

    def load_favorite_sounds(self):
        return self.helper.load_favorite_sounds()

    def load_toasts(self):
        return self.helper.load_toasts()

    def get_random_toast(self):
        return self.helper.get_random_toast()
