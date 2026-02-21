import json
import uuid
from pathlib import Path

import flet as ft

from core.helpers.factories.settings_sync import create_settings_sync_helper
from core.settings.base.radio_stations import BaseRadioStationsSettings


class WebRadioStationsSettings(BaseRadioStationsSettings):
    def __init__(self, page: ft.Page):
        self.page = page
        self.settings_sync = create_settings_sync_helper()

    def load_radio_stations(self):
        stations = self.page.client_storage.get("stations")
        if stations is None:
            path = Path.cwd() / "settings" / "radio-stations.json"
            with open(path, "r") as f:
                data = json.load(f)

            self.page.client_storage.set("stations", data)

        return self.page.client_storage.get("stations") or []

    def add_station(self, station):
        station["id"] = str(uuid.uuid4())
        station["favorite"] = False

        stations = self.load_radio_stations()
        stations.append(station)
        self.page.client_storage.set("stations", stations)

    def delete_station(self, station):
        data = [
            obj
            for obj in self.load_radio_stations()
            if obj.get("id") != station.get("id")
        ]
        self.page.client_storage.set("stations", data)

    def set_favorite_station(self, fav_station):
        stations = self.load_radio_stations()
        for station in stations:
            station["favorite"] = False

        for station in stations:
            if station["id"] == fav_station["id"]:
                station["favorite"] = True
                break

    def get_favorite_station(self) -> object | None:
        stations = self.load_radio_stations()
        for station in stations:
            if station["favorite"]:
                return station

        return None
