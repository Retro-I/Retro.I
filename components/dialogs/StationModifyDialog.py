import flet as ft

from components.dialogs.StationDeleteDialog import StationDeleteDialog
from helper.PageState import PageState
from helper.Stations import Stations

stations_helper = Stations()


class StationModifyDialog(ft.AlertDialog):
    station = None
    submit_callback = None

    def __init__(self):
        super().__init__()

        self.station_delete_dialog = StationDeleteDialog()
        PageState.page.add(self.station_delete_dialog)

        self.title = ft.Text("Sender bearbeiten")
        self.actions = [
            ft.TextButton("Löschen", on_click=lambda e: self.on_delete()),
            ft.FilledButton(
                "Als Lieblingssender setzen", on_click=lambda e: self.on_set_favorite()
            ),
        ]

    def open_dialog(self, station, submit_callback):
        self.open = True
        self.station = station
        self.submit_callback = submit_callback
        self.update()

    def on_delete(self):
        self.station_delete_dialog.open_dialog(self.station, self.submit_callback)

    def on_set_favorite(self):
        stations_helper.set_favorite_station(self.station)
        self.close()
        self.submit_callback()

    def close(self):
        self.open = False
        self.update()
