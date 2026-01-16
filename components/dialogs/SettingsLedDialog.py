import flet as ft

from helper.Strip import Strip
from helper.StripSettingsHelper import StripSettingsHelper

strip = Strip()
settings_helper = StripSettingsHelper()


class SettingsLedDialog(ft.AlertDialog):
    def __init__(self):
        super().__init__()

        self.title = ft.Text("LED-Streifen")
        self.content = ft.Column(
            alignment=ft.MainAxisAlignment.CENTER,
            width=500,
            tight=True,
            controls=[
                ft.Switch(
                    "LED-Streifen einschalten",
                    label_style=ft.TextStyle(size=18),
                    on_change=lambda e: strip.toggle_strip(),
                    value=settings_helper.is_strip_active(),
                ),
                ft.Divider(),
                ft.Column(
                    [
                        ft.Text("Helligkeit:", style=ft.TextStyle(size=20)),
                        ft.Slider(
                            on_change=lambda e: strip.change_brightness(
                                e.control.value
                            ),
                            min=0,
                            max=100,
                            value=settings_helper.get_curr_brightness(),
                            expand=True,
                        ),
                    ]
                ),
            ],
        )

    def open_dialog(self):
        self.open = True
        self.update()
