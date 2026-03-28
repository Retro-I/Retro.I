import flet as ft

from helper.Stations import Stations

stations_helper = Stations()


class StationDeleteDialog(ft.AlertDialog):
    station = None
    submit_callback = None

    def __init__(self):
        super().__init__()

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
        stations_helper.delete_station(self.station)
        self.submit_callback()
        self.close()

    def close(self):
        self.open = False
        self.update()
