import threading
import time

import flet as ft

from components.dialogs.credits import Credits
from components.dialogs.documentation import Documentation
from components.dialogs.info import Info
from components.scrollbar import with_scrollbar_space
from core.factories.settings_factories import (
    create_developer_mode_settings as developer_settings,
)


class SettingsInfoDialog(ft.AlertDialog):
    def __init__(self):
        super().__init__()
        self.info = Info()

        self.content = ft.Column(
            width=500,
            tight=True,
            controls=[
                ft.Tabs(
                    selected_index=0,
                    length=3,
                    animation_duration=300,
                    expand=True,
                    content=ft.Column(
                        [
                            ft.TabBar(
                                tabs=[
                                    ft.Tab(
                                        label="         Systeminfo         "
                                    ),
                                    ft.Tab(
                                        label="         Dokumentation         "
                                    ),
                                    ft.Tab(label="         Credits         "),
                                ]
                            ),
                            ft.TabBarView(
                                controls=[
                                    ft.Container(
                                        content=with_scrollbar_space(self.info),
                                        alignment=ft.Alignment.CENTER,
                                        visible=(
                                            developer_settings().is_developer_mode_active()  # noqa:E501
                                        ),
                                    ),
                                    ft.Container(
                                        content=Documentation(),
                                        alignment=ft.Alignment.CENTER,
                                    ),
                                    ft.Container(
                                        content=Credits(),
                                        alignment=ft.Alignment.CENTER,
                                    ),
                                ],
                                expand=True,
                            ),
                        ]
                    ),
                ),
            ],
        )

    def open_dialog(self):
        self.open = True
        self.update()

        def _retrieve_system_info():
            while self.open:
                self.info.set_system_info()

                time.sleep(0.5)

        process = threading.Thread(target=_retrieve_system_info)
        process.start()
