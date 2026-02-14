import flet as ft

from core.factories.strip_factory import create_strip_state
from helper.StripSettingsHelper import StripSettingsHelper

settings_helper = StripSettingsHelper()


class SettingsLedDialog(ft.AlertDialog):
    strip_state = create_strip_state()

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
                    on_change=self.strip_state.toggle_strip,
                    value=settings_helper.is_strip_active(),
                ),
                ft.Divider(),
                ft.Column(
                    [
                        ft.Text("Helligkeit:", style=ft.TextStyle(size=20)),
                        ft.Slider(
                            on_change=lambda e: (
                                self.strip_state.change_brightness(
                                    e.control.value
                                )
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
