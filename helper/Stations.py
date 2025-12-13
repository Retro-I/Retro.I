import json
import uuid

from helper.Audio import Audio
from helper.ColorHelper import ColorHelper
from helper.Constants import Constants
from helper.SettingsSyncHelper import SettingsSyncHelper

c = Constants()
color_helper = ColorHelper()
settings_sync_helper = SettingsSyncHelper()
audio_helper = Audio()


class Stations:
    STATION_SETTING = "radio-stations.json"
    STATIONS_SETTINGS_PATH = f"{Constants.settings_path()}/{STATION_SETTING}"

    def load_radio_stations(self):
        def _get_data():
            with open(self.STATIONS_SETTINGS_PATH) as file:
                data = json.load(file)
                return data

        try:
            return _get_data()
        except Exception:
            settings_sync_helper.repair_settings_file(self.STATION_SETTING)
            return _get_data()

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
