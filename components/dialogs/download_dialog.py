import flet as ft

from core.helpers.factories.system import create_system_helper


class DownloadDialog(ft.AlertDialog):
    text = ft.TextSpan(
        "", style=ft.TextStyle(weight=ft.FontWeight.BOLD, size=16)
    )
    info = ft.Text()

    def __init__(self):
        super().__init__()

        self.system_helper = create_system_helper()

        self.content = ft.Column(
            [
                ft.ProgressRing(),
                ft.Text(
                    spans=[
                        ft.TextSpan(
                            "Update für Version ", style=ft.TextStyle(size=16)
                        ),
                        self.text,
                        ft.TextSpan(
                            " wird durchgeführt...", style=ft.TextStyle(size=16)
                        ),
                        self.info,
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

    def update_info(self, text: str):
        self.info.text = text
        self.info.update()

    def close_dialog(self):
        self.open = False
        self.update()

    def cancel(self):
        self.system_helper.cancel_revision_update()
        self.close_dialog()
