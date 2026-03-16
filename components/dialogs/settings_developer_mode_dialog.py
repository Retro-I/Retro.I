import flet as ft

from components.dialogs.updates_restart_dialog import UpdatesRestartDialog
from core.factories.settings_factories import (
    create_developer_mode_settings as developer_settings,
)
from helper.page_state import PageState


class SettingsDeveloperModeDialog(ft.AlertDialog):
    def __init__(self):
        super().__init__()

        self.restart_dialog = UpdatesRestartDialog()
        PageState.page.add(self.restart_dialog)

        self.title = ft.Text("Entwicklermodus")
        self.content = ft.Column(
            alignment=ft.MainAxisAlignment.CENTER,
            width=500,
            tight=True,
            controls=[
                ft.Switch(
                    label="Entwicklermodus einschalten (Neustart erforderlich!)",
                    label_text_style=ft.TextStyle(size=18),
                    on_change=self.on_toggle,
                    value=(developer_settings().is_developer_mode_active()),
                ),
            ],
        )

    def on_toggle(self, control):
        developer_settings().toggle_developer_mode_active(control)
        self.restart_dialog.open_dialog()

    def open_dialog(self):
        self.open = True
        self.update()
