import flet as ft

from components.IconBtn import IconBtn
from helper.SystemHelper import SystemHelper

system_helper = SystemHelper()


class UpdatesRestartDialog(ft.AlertDialog):
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
                            text="System neustarten",
                            icon=ft.Icons.RESTART_ALT,
                            on_click=system_helper.restart_system,
                        ),
                        IconBtn(
                            text="App neustarten",
                            icon=ft.Icons.REFRESH,
                            on_click=system_helper.restart_app,
                        ),
                    ],
                ),
            ],
        )

    def open_dialog(self):
        self.open = True
        self.update()
