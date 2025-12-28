import flet as ft

from components.IconBtn import IconBtn
from helper.SystemHelper import SystemHelper

system_helper = SystemHelper()


class SettingsShutdownDialog(ft.AlertDialog):
    def __init__(self):
        super().__init__()

        self.content = ft.Column(
            alignment=ft.MainAxisAlignment.CENTER,
            width=500,
            tight=True,
            controls=[
                ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=75,
                    controls=[
                        IconBtn(
                            text="Herunterfahren",
                            icon=ft.Icons.POWER_SETTINGS_NEW,
                            on_click=system_helper.shutdown_system,
                        ),
                        IconBtn(
                            text="Neustarten",
                            icon=ft.Icons.RESTART_ALT,
                            on_click=system_helper.restart_system,
                        ),
                    ],
                ),
            ],
        )

    def open_dialog(self):
        self.open = True
        self.update()
