import flet as ft

from helper.Constants import Constants
from helper.Stations import Stations

stations_helper = Stations()


class StationDeleteDialog(ft.AlertDialog):
    submit_callback = None

    def __init__(self):
        super().__init__()

        self.title = ft.Text("Sender löschen?")
        self.actions_alignment = ft.MainAxisAlignment.SPACE_BETWEEN
        self.actions = [
            ft.TextButton("Abbrechen", on_click=lambda e: self.close()),
            ft.FilledButton("Löschen", on_click=lambda e: self.submit()),
        ]

    def submit(self):
        stations_helper.delete_station(Constants.current_station_index_to_delete)
        self.submit_callback()
        self.close()

    def open_dialog(self, submit_callback):
        self.open = True
        self.submit_callback = submit_callback
        self.update()

    def close(self):
        self.open = False
        self.update()
