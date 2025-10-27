import flet as ft

from components.VolumeInputField import VolumeInputField
from helper.Stations import Stations

stations_helper = Stations()


class SettingsSystemDialog(ft.AlertDialog):
    def __init__(self):
        super().__init__()

        self.title = ft.Text("System")
        self.content = ft.Column(
            alignment=ft.MainAxisAlignment.CENTER,
            width=500,
            tight=True,
            controls=[
                VolumeInputField(),
                ft.Divider(),
                ft.Switch(
                    "Lieblingsradiosender nach Systemstart abspielen",
                    label_style=ft.TextStyle(size=18),
                    on_change=lambda e: self.toggle_enable_autoplay(),
                    value=stations_helper.is_default_station_autoplay_enabled(),
                ),
            ],
        )

    def toggle_enable_autoplay(self):
        stations_helper.toggle_default_station_autoplay()

    def open_dialog(self):
        self.open = True
        self.update()

    def close_dialog(self):
        self.open = False
        self.update()
