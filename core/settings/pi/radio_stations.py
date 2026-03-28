from core.settings.base.radio_stations import BaseRadioStationsSettings
from helper.Stations import Stations


class PiRadioStationsSettings(BaseRadioStationsSettings):
    def __init__(self):
        self.settings = Stations()

    def load_radio_stations(self):
        return self.settings.load_radio_stations()

    def add_station(self, station):
        self.settings.add_station(station)

    def delete_station(self, station):
        self.settings.delete_station(station)

    def set_favorite_station(self, fav_station):
        self.settings.set_favorite_station(fav_station)

    def get_favorite_station(self) -> object | None:
        return self.settings.get_favorite_station()
