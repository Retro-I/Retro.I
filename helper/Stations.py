import csv
import json
import uuid

from helper.ColorHelper import ColorHelper
from helper.Constants import Constants

c = Constants()
color_helper = ColorHelper()


class Stations:
    STATIONS_FILE_PATH = f"{c.pwd()}/assets/radio-stations.json"
    SETTINGS_FILE_PATH = f"{c.pwd()}/settings/default-station-settings.csv"

    def load_radio_stations(self):
        with open(self.STATIONS_FILE_PATH) as file:
            data = json.load(file)
            return data

    def add_station(self, station):
        station["id"] = str(uuid.uuid4())
        station["favorite"] = False

        if station["name"] != "":
            station["color"] = color_helper.extract_color(station["logo"])

        with open(self.STATIONS_FILE_PATH, "r+") as file:
            file_data = json.load(file)
            file_data.append(station)
            file.seek(0)
            json.dump(file_data, file, indent=4)

    def delete_station(self, index):
        with open(self.STATIONS_FILE_PATH, "r+") as file:
            file_data = json.load(file)
            file_data.pop(index)

        self._write_to_file(file_data)

    def set_favorite_station(self, fav_station):
        stations = self.load_radio_stations()

        for station in stations:
            station["favorite"] = False

        for station in stations:
            if station["id"] == fav_station["id"]:
                station["favorite"] = True
                break

        self._write_to_file(stations)

    def get_favorite_station(self) -> object | None:
        stations = self.load_radio_stations()
        for station in stations:
            if station["favorite"]:
                return station

        return None

    def is_default_station_autoplay_enabled(self) -> bool:
        with open(self.SETTINGS_FILE_PATH) as file:
            return bool(int(file.read()))

    def toggle_default_station_autoplay(self):
        val = int(not self.is_default_station_autoplay_enabled())

        with open(self.SETTINGS_FILE_PATH, "w", newline="") as csvfile:
            writer = csv.writer(csvfile, delimiter=";", quotechar=" ", quoting=csv.QUOTE_MINIMAL)
            writer.writerow([val])

    def _write_to_file(self, data):
        with open(self.STATIONS_FILE_PATH, "w") as file:
            file.write(json.dumps(data, sort_keys=True, indent=4, separators=(",", ": ")))
