import flet as ft

from core.helpers.factories.qrcode import create_qrcode_helper
from helper.RevisionHelper import RevisionHelper

revision_helper = RevisionHelper()


class Documentation(ft.Column):
    def __init__(self):
        super().__init__()

        self.qrcode_helper = create_qrcode_helper()

        self.expand = True
        self.controls = [
            ft.Text(
                spans=[
                    ft.TextSpan(
                        "Die Dokumenatation zum Projekt findest du unter "
                    ),
                    ft.TextSpan(
                        "https://docs.retroi.de",
                        style=ft.TextStyle(weight=ft.FontWeight.BOLD),
                    ),
                ],
                size=20,
            ),
            ft.Divider(),
            ft.Row(
                [
                    ft.Image(
                        src_base64=self.qrcode_helper.str_to_qr_code(
                            "https://docs.retroi.de"
                        ),
                        width=200,
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            ft.Divider(),
        ]
