import flet as ft

from components.IconBtn import IconBtn
from core.helpers.factories.system import create_system_helper


class SettingsAppControlDialog(ft.AlertDialog):
    def __init__(self):
        super().__init__()

        self.system_helper = create_system_helper()

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
                            text="App beenden",
                            icon=ft.Icons.LOGOUT,
                            on_click=self.system_helper.stop_app,
                        ),
                        IconBtn(
                            text="App neustarten",
                            icon=ft.Icons.REFRESH,
                            on_click=self.system_helper.restart_app,
                        ),
                    ],
                ),
            ],
        )

    def open_dialog(self):
        self.open = True
        self.update()
