import flet as ft

from helper.SystemHelper import SystemHelper

system_helper = SystemHelper()


class SettingsAppControlDialog(ft.AlertDialog):
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
                                    ft.icons.HIGHLIGHT_OFF,
                                    icon_size=75,
                                    on_click=lambda e: system_helper.stop_app(),
                                ),
                                ft.Text(
                                    "App beenden",
                                    text_align=ft.TextAlign.CENTER,
                                    style=ft.TextStyle(size=18),
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        ),
                        ft.Column(
                            [
                                ft.IconButton(
                                    ft.icons.REFRESH,
                                    icon_size=75,
                                    on_click=lambda e: system_helper.restart_app(),
                                ),
                                ft.Text(
                                    "App neustarten",
                                    text_align=ft.TextAlign.CENTER,
                                    style=ft.TextStyle(size=18),
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        ),
                    ],
                ),
            ],
        )

    def open_dialog(self):
        self.open = True
        self.update()
