import threading
import time

import flet as ft

from helper.LogsHelper import LogsHelper

logs_helper = LogsHelper()


class SettingsLogsDialog(ft.AlertDialog):
    def __init__(self):
        super().__init__()

        self.get_logs = False
        self.logs_text_field = ft.TextField(
            multiline=True,
            read_only=True,
            expand=True,
            clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
            text_style=ft.TextStyle(
                font_family="monospace",
                size=12,
            ),
        )

        self.title = ft.Text("Logs")
        self.on_dismiss = lambda e: self.close_dialog()
        self.content = ft.Container(
            expand=True,
            content=self.logs_text_field,
        )
        self.actions = [
            ft.FilledButton("Abbrechen", on_click=lambda e: self.close_dialog())
        ]

    def update_logs(self):
        while self.get_logs:
            self.logs_text_field.value = logs_helper.get_logs()
            self.logs_text_field.update()
            time.sleep(0.5)

    def open_dialog(self):
        self.get_logs = True
        logs_thread = threading.Thread(target=self.update_logs)
        logs_thread.start()

        self.open = True
        self.update()

    def close_dialog(self):
        self.get_logs = False
        self.open = False
        self.update()
