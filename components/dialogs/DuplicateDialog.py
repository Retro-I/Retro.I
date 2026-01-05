import flet as ft


class DuplicateDialog(ft.AlertDialog):
    name_span = ft.TextSpan("Radiosender")

    def __init__(self):
        super().__init__()

        self.title = ft.Text(
            spans=[self.name_span, ft.TextSpan(" ist bereits in der Liste!")],
            size=20,
        )
        self.actions = [ft.FilledButton("Ok", on_click=lambda e: self.close())]
        self.actions_alignment = ft.MainAxisAlignment.END

    def open_dialog(self, name):
        self.open = True
        self.update()
        self.name_span.text = name
        self.name_span.update()

    def close(self):
        self.open = False
        self.update()
