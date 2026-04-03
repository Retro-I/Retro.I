class BaseRadioStationsSettings:
    def load_radio_stations(self):
        raise NotImplementedError

    def add_station(self, station):
        raise NotImplementedError

    def delete_station(self, station):
        raise NotImplementedError

    def set_favorite_station(self, fav_station):
        raise NotImplementedError

    def get_favorite_station(self) -> object | None:
        raise NotImplementedError
