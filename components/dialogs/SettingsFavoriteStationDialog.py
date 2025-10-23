import flet as ft

from helper.Stations import Stations

stations_helper = Stations()


class SettingsFavoriteStationDialog(ft.AlertDialog):
    def __init__(self):
        super().__init__()

        self.content = ft.Column(
            alignment=ft.MainAxisAlignment.CENTER,
            width=500,
            tight=True,
            controls=[
                ft.Switch(
                    "Lieblingsradiosender nach Systemstart abspielen",
                    label_position=ft.LabelPosition.LEFT,
                    label_style=ft.TextStyle(size=20),
                    on_change=lambda e: self.toggle_enable_autoplay(),
                    value=stations_helper.is_default_station_autoplay_enabled(),
                ),
            ],
        )

    def toggle_enable_autoplay(self):
        stations_helper.toggle_default_station_autoplay()
        self.close_dialog()

    def open_dialog(self):
        self.open = True
        self.update()

    def close_dialog(self):
        self.open = False
        self.update()
