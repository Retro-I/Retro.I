from core.settings.base.radio_stations import BaseRadioStationsSettings


class WebRadioStationsSettings(BaseRadioStationsSettings):
    def load_radio_stations(self):
        return [
            {
                "color": "#00A1D6",
                "favorite": False,
                "id": "2a756cf7-35a4-469e-ad09-0afce7913214",
                "logo": "https://api.ardmediathek.de/image-service/images"
                "/urn:ard:image:b366004f6196d70c?w=512",
                "name": "Bayern 1",
                "src": "https://dispatcher.rndfnk.com/br/br1/nbopf/mp3/mid",
            }
        ]  # TODO - muss noch anders gemacht werden

    def add_station(self, station):
        pass

    def delete_station(self, station):
        pass

    def set_favorite_station(self, fav_station):
        pass

    def get_favorite_station(self) -> object | None:
        return None
