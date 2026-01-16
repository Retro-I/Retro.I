import flet as ft

from helper import QrCodeHelper
from helper.RevisionHelper import RevisionHelper
from helper.SystemHelper import SystemHelper

system_helper = SystemHelper()
revision_helper = RevisionHelper()


class Documentation(ft.Column):
    def __init__(self):
        super().__init__()

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
                        src_base64=QrCodeHelper.str_to_qr_code(
                            "https://docs.retroi.de"
                        )
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
        ]
