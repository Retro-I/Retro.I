import json
import uuid

from core.helpers.factories.color import create_color_helper
from core.helpers.factories.settings_sync import create_settings_sync_helper
from helper.Constants import Constants

c = Constants()


class Stations:
    STATION_SETTING = "radio-stations.json"
    STATIONS_SETTINGS_PATH = f"{Constants.settings_path()}/{STATION_SETTING}"

    def __init__(self):
        self.color_helper = create_color_helper()
        self.settings_sync_helper = create_settings_sync_helper()

    def load_radio_stations(self):
        def _get_data():
            with open(self.STATIONS_SETTINGS_PATH) as file:
                data = json.load(file)
                return data

        try:
            return _get_data()
        except Exception:
            self.settings_sync_helper.reset_settings_file(self.STATION_SETTING)
            return _get_data()

    def add_station(self, station):
        station["id"] = str(uuid.uuid4())
        station["favorite"] = False

        if station["name"] != "":
            station["color"] = self.color_helper.extract_color(station["logo"])

        with open(self.STATIONS_SETTINGS_PATH, "r+") as file:
            data = json.load(file)
            data.append(station)
            file.seek(0)
            json.dump(data, file, indent=4)

    def delete_station(self, station):
        data = [
            obj
            for obj in self.load_radio_stations()
            if obj.get("id") != station.get("id")
        ]

        with open(self.STATIONS_SETTINGS_PATH, "r+") as file:
            file.seek(0)
            json.dump(data, file, indent=4)
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
