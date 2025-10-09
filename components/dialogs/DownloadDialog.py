import flet as ft


class DownloadDialog(ft.AlertDialog):
    text = ft.TextSpan("", style=ft.TextStyle(weight=ft.FontWeight.BOLD))

    def __init__(self):
        super().__init__()

        self.title = ft.Text(
            spans=[ft.TextSpan("Update für Version "), self.text, ft.TextSpan(" wird heruntergeladen...")]
        )
        self.actions = [ft.FilledButton("Ok", on_click=lambda e: self.close_dialog())]
        self.actions_alignment = ft.MainAxisAlignment.END

    def open_dialog(self, revision):
        self.text.value = revision
        self.text.update()
        self.open = True
        self.update()

    def close_dialog(self):
        self.open = False
        self.update()
