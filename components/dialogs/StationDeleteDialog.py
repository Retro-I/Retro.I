import flet as ft

from core.settings.factories.radio_stations import create_radio_stations_settings


class StationDeleteDialog(ft.AlertDialog):
    station = None
    submit_callback = None

    def __init__(self):
        super().__init__()

        self.stations = create_radio_stations_settings()

        self.title = ft.Text("Sender löschen?")
        self.actions_alignment = ft.MainAxisAlignment.SPACE_BETWEEN
        self.actions = [
            ft.TextButton("Abbrechen", on_click=lambda e: self.close()),
            ft.FilledButton("Löschen", on_click=lambda e: self.submit()),
        ]

    def open_dialog(self, station, submit_callback):
        self.open = True
        self.station = station
        self.submit_callback = submit_callback
        self.update()

    def submit(self):
        self.stations.delete_station(self.station)
        self.submit_callback()
        self.close()

    def close(self):
        self.open = False
        self.update()
