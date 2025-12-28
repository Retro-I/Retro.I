import flet as ft

from components.IconBtn import IconBtn
from helper.SettingsSyncHelper import SettingsSyncHelper
from helper.SystemHelper import SystemHelper

system_helper = SystemHelper()
settings_sync_helper = SettingsSyncHelper()


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
                        IconBtn(
                            text="App beenden",
                            icon=ft.Icons.LOGOUT,
                            on_click=system_helper.stop_app,
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
