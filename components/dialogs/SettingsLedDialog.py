import flet as ft

from core.factories.strip_factory import create_strip_state
from core.settings.factories.strip import create_strip_settings


class SettingsLedDialog(ft.AlertDialog):

    def __init__(self):
        super().__init__()

        self.strip_state = create_strip_state()
        self.strip_settings = create_strip_settings()

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
                    value=self.strip_settings.is_strip_active(),
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
                            value=self.strip_settings.get_curr_brightness(),
                            expand=True,
                        ),
                    ]
                ),
            ],
        )

    def open_dialog(self):
        self.open = True
        self.update()
