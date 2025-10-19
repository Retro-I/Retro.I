import flet as ft

from components.dialogs.UpdatesRestartDialog import UpdatesRestartDialog
from helper.PageState import PageState


class SuccessDialog(ft.AlertDialog):
    text = ft.Text("")
    display_icon = ft.Icon(ft.icons.DOWNLOAD_DONE, size=36, visible=False)

    def __init__(self):
        super().__init__()
        self.updates_restart_dialog = UpdatesRestartDialog()

        PageState.page.add(self.updates_restart_dialog)

        self.title = ft.Text("")
        self.content = ft.Column(
            [
                self.display_icon,
                self.text,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            tight=True,
        )
        self.modal = True
        self.actions = [
            ft.TextButton("Neustart", on_click=lambda e: self.updates_restart_dialog.open_dialog()),
            ft.FilledButton("Ok", on_click=lambda e: self.close_dialog())
        ]
        self.actions_alignment = ft.MainAxisAlignment.SPACE_BETWEEN
        self.actions_alignment = ft.MainAxisAlignment.END

    def open_dialog(self, title: str, msg: str, show_icon: bool = False):
        self.title.value = title
        self.title.update()

        self.display_icon.visible = show_icon
        self.display_icon.update()

        self.text.value = msg
        self.text.update()
        self.open = True
        self.update()

    def close_dialog(self):
        self.open = False
        self.update()
