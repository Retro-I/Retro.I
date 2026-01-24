import threading
import time

import flet as ft

from components.dialogs.Credits import Credits
from components.dialogs.Documentation import Documentation
from components.dialogs.Info import Info
from components.Scrollbar import with_scrollbar_space
from helper.DeveloperModeHelper import DeveloperModeHelper


class SettingsInfoDialog(ft.AlertDialog):
    def __init__(self):
        super().__init__()
        self.info = Info()

        self.content = ft.Column(
            width=500,
            tight=True,
            controls=[
                ft.Tabs(
                    animation_duration=300,
                    tab_alignment=ft.TabAlignment.CENTER,
                    expand=True,
                    tabs=[
                        ft.Tab(
                            text="            Info            ",
                            content=ft.Column(
                                alignment=ft.MainAxisAlignment.CENTER,
                                horizontal_alignment=(
                                    ft.CrossAxisAlignment.CENTER,
                                ),
                                controls=[with_scrollbar_space(self.info)],
                            ),
                            visible=(
                                DeveloperModeHelper.is_developer_mode_active(),
                            ),
                        ),
                        ft.Tab(
                            text="        Dokumentation        ",
                            content=ft.Column(
                                horizontal_alignment=(
                                    ft.CrossAxisAlignment.CENTER,
                                ),
                                controls=[Documentation()],
                            ),
                        ),
                        ft.Tab(
                            text="           Credits           ",
                            content=ft.Column(
                                horizontal_alignment=(
                                    ft.CrossAxisAlignment.CENTER,
                                ),
                                controls=[Credits()],
                            ),
                        ),
                    ],
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
