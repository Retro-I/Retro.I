import flet as ft


class DownloadDialog(ft.AlertDialog):
    text = ft.TextSpan("", style=ft.TextStyle(weight=ft.FontWeight.BOLD))

    def __init__(self):
        super().__init__()

        self.content = ft.Column(
            [
                ft.ProgressRing(),
                ft.Text(
                    spans=[ft.TextSpan("Updates für Version "), self.text, ft.TextSpan(" werden heruntergeladen...")]
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
        self.modal = True

    def open_dialog(self, revision):
        self.text.text = revision
        self.text.update()
        self.open = True
        self.update()

    def close_dialog(self):
        self.open = False
        self.update()
