import asyncio

import flet as ft

from core.factories.helper_factories import create_logs_helper


class SettingsLogsDialog(ft.AlertDialog):
    def __init__(self):
        super().__init__()

        self.logs_helper = create_logs_helper()

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

    async def update_logs(self):
        while self.open:
            self.logs_text_field.value = self.logs_helper.get_logs()
            self.logs_text_field.update()
            await asyncio.sleep(0.5)

    def open_dialog(self):
        self.open = True
        self.page.run_task(self.update_logs)
        self.update()

    def close_dialog(self):
        self.open = False
        self.update()
