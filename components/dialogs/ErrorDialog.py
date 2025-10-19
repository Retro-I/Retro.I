import flet as ft


class ErrorDialog(ft.AlertDialog):
    text = ft.Text("")
    display_icon = ft.Icon(ft.icons.ERROR, size=36, visible=False)

    def __init__(self):
        super().__init__()

        self.title = ft.Text("Ein Fehler ist aufgetreten!")
        self.content = ft.Column(
            [
                self.display_icon,
                self.text
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            tight=True,
        )
        self.modal = True
        self.actions = [ft.FilledButton("Ok", on_click=lambda e: self.close_dialog())]
        self.actions_alignment = ft.MainAxisAlignment.END

    def open_dialog(self, msg: str, show_icon: bool = False):
        self.display_icon.visible = show_icon
        self.display_icon.update()

        self.text.value = msg
        self.text.update()
        self.open = True
        self.update()

    def close_dialog(self):
        self.open = False
        self.update()
