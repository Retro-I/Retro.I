import flet as ft

from components.dialogs.UpdatesRestartDialog import UpdatesRestartDialog
from helper.PageState import PageState
from helper.SystemHelper import SystemHelper

system_helper = SystemHelper()


class SettingsDisplayDialog(ft.AlertDialog):
    def __init__(self):
        super().__init__()
        self.updates_restart_dialog = UpdatesRestartDialog()

        PageState.page.add(self.updates_restart_dialog)

        self.content = ft.Column(
            alignment=ft.MainAxisAlignment.CENTER,
            width=500,
            tight=True,
            controls=[
                ft.Switch(
                    "Scrollbar anzeigen",
                    label_position=ft.LabelPosition.LEFT,
                    label_style=ft.TextStyle(size=20),
                    on_change=lambda e: self.toggle_enable_scrollbar(),
                    value=system_helper.is_scrollbar_enabled(),
                ),
            ],
        )

    def toggle_enable_scrollbar(self):
        system_helper.toggle_scrollbar_enabled()
        self.close_dialog()
        self.updates_restart_dialog.open_dialog()

    def open_dialog(self):
        self.open = True
        self.update()

    def close_dialog(self):
        self.open = False
        self.update()
