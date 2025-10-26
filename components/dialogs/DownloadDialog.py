import flet as ft

from helper.SystemHelper import SystemHelper

system_helper = SystemHelper()


class DownloadDialog(ft.AlertDialog):
    text = ft.TextSpan("", style=ft.TextStyle(weight=ft.FontWeight.BOLD, size=16))

    def __init__(self):
        super().__init__()

        self.content = ft.Column(
            [
                ft.ProgressRing(),
                ft.Text(
                    spans=[
                        ft.TextSpan("Updates für Version ", style=ft.TextStyle(size=16)),
                        self.text,
                        ft.TextSpan(" werden heruntergeladen...", style=ft.TextStyle(size=16)),
                    ],
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            tight=True,
        )
        self.actions = [
            ft.TextButton("Abbrechen", on_click=lambda e: self.cancel())
        ]
        self.modal = True

    def open_dialog(self, revision):
        self.text.text = revision["name"]
        self.text.update()
        self.open = True
        self.update()

    def close_dialog(self):
        self.open = False
        self.update()

    def cancel(self):
        system_helper.cancel_revision_update()
        self.close_dialog()
