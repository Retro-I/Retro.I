import flet as ft

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
                        ft.Column(
                            [
                                ft.IconButton(
                                    ft.icons.LOGOUT,
                                    icon_size=75,
                                    on_click=lambda e: system_helper.shutdown_system(),
                                ),
                                ft.Text(
                                    "Herunterfahren",
                                    text_align=ft.TextAlign.CENTER,
                                    style=ft.TextStyle(size=18),
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                        ),
                        ft.Column(
                            [
                                ft.IconButton(
                                    ft.icons.RESTART_ALT,
                                    icon_size=75,
                                    on_click=lambda e: system_helper.restart_system(),
                                ),
                                ft.Text(
                                    "Neustarten",
                                    text_align=ft.TextAlign.CENTER,
                                    style=ft.TextStyle(size=18),
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                        ),
                    ],
                ),
            ],
        )

    def open_dialog(self):
        self.open = True
        self.update()
