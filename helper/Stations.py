import json
import uuid

from helper.ColorHelper import ColorHelper
from helper.Constants import Constants

c = Constants()
color_helper = ColorHelper()


class Stations:
    STATIONS_SETTINGS_PATH = f"{c.settings_path()}/radio-stations.json"
    AUDIO_SETTINGS_PATH = f"{c.settings_path()}/audio-settings.json"

    def load_radio_stations(self):
        with open(self.STATIONS_SETTINGS_PATH) as file:
            data = json.load(file)
            return data

    def add_station(self, station):
        station["id"] = str(uuid.uuid4())
        station["favorite"] = False

        if station["name"] != "":
            station["color"] = color_helper.extract_color(station["logo"])

        with open(self.STATIONS_SETTINGS_PATH, "r+") as file:
            data = json.load(file)
            data.append(station)
            file.seek(0)
            json.dump(data, file, indent=4)

    def delete_station(self, index):
        with open(self.STATIONS_SETTINGS_PATH, "r+") as file:
            data = json.load(file)
            data.pop(index)
            file.seek(0)
            json.dump(data, file)
            file.truncate()

    def set_favorite_station(self, fav_station):
        stations = self.load_radio_stations()

        for station in stations:
            station["favorite"] = False

        for station in stations:
            if station["id"] == fav_station["id"]:
                station["favorite"] = True
                break

        with open(self.STATIONS_SETTINGS_PATH, "r+") as file:
            file.seek(0)
            json.dump(stations, file, indent=4)
            file.truncate()

    def get_favorite_station(self) -> object | None:
        stations = self.load_radio_stations()
        for station in stations:
            if station["favorite"]:
                return station

        return None

    def is_default_station_autoplay_enabled(self) -> bool:
        with open(self.AUDIO_SETTINGS_PATH) as file:
            file_data = json.load(file)
            return file_data["enableAutoplay"]

    def toggle_default_station_autoplay(self):
        with open(self.AUDIO_SETTINGS_PATH, "r+") as file:
            data = json.load(file)
            data["enableAutoplay"] = not self.is_default_station_autoplay_enabled()
            file.seek(0)
            json.dump(data, file, indent=4)
            file.truncate()
