import flet as ft

from components.IconBtn import IconBtn
from core.helpers.factories.system import create_system_helper


class UpdatesRestartDialog(ft.AlertDialog):
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
                            text="System neustarten",
                            icon=ft.Icons.RESTART_ALT,
                            on_click=self.system_helper.restart_system,
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
