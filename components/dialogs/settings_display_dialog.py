import flet as ft

from components.dialogs.admin_password_dialog import AdminPasswordDialog
from components.dialogs.splashscreen_dialog import SplashscreenDialog
from components.dialogs.updates_restart_dialog import UpdatesRestartDialog
from core.factories.helper_factories import create_system_helper
from core.factories.settings_factories import (
    create_party_mode_settings,
    create_scrollbar_settings,
)
from helper.page_state import PageState


class SettingsDisplayDialog(ft.AlertDialog):
    def __init__(self):
        super().__init__()
        self.party_mode_settings = create_party_mode_settings()

        self.updates_restart_dialog = UpdatesRestartDialog()
        self.splashscreen_dialog = SplashscreenDialog()
        self.admin_password_dialog = AdminPasswordDialog(
            self.updates_restart_dialog.open_dialog
        )

        self.system_helper = create_system_helper()
        self.scrollbar_settings_helper = create_scrollbar_settings()

        PageState.page.add(self.updates_restart_dialog)
        PageState.page.add(self.admin_password_dialog)

        self.soundboard_switch = ft.Switch(
            label="Soundboard anzeigen (Neustart erforderlich!)",
            label_text_style=ft.TextStyle(size=18),
            on_change=lambda e: self.open_admin_password_dialog(),
            value=self.party_mode_settings.is_party_mode(),
        )

        self.title = ft.Text("Anzeige")
        self.content = ft.Column(
            alignment=ft.MainAxisAlignment.CENTER,
            width=500,
            tight=True,
            controls=[
                ft.Switch(
                    label="Scrollbar anzeigen (Neustart erforderlich!)",
                    label_text_style=ft.TextStyle(size=18),
                    on_change=lambda e: self.toggle_enable_scrollbar(),
                    value=self.scrollbar_settings_helper.is_scrollbar_enabled(),
                ),
                ft.Divider(),
                self.soundboard_switch,
                ft.Divider(),
                ft.Column(
                    [
                        ft.Text(
                            "Bildschirm-Helligkeit:",
                            style=ft.TextStyle(size=20),
                        ),
                        ft.Slider(
                            min=10,
                            max=100,
                            divisions=19,
                            label="{value}%",
                            value=self.system_helper.get_curr_brightness(),
                            on_change=self.slider_changed,
                            expand=True,
                        ),
                    ]
                ),
                ft.Divider(),
                ft.TextButton(
                    "Splashscreen ändern",
                    style=ft.ButtonStyle(text_style=ft.TextStyle(size=20)),
                    on_click=lambda e: self.open_splashscreen_dialog(),
                    icon=ft.Icons.OPEN_IN_NEW,
                ),
            ],
        )

    def toggle_enable_scrollbar(self):
        self.scrollbar_settings_helper.toggle_scrollbar_enabled()
        self.close_dialog()
        self.updates_restart_dialog.open_dialog()

    def slider_changed(self, e):
        self.system_helper.change_screen_brightness(e.control.value)

    def open_splashscreen_dialog(self):
        PageState.page.show_dialog(self.splashscreen_dialog)

    def open_admin_password_dialog(self):
        self.admin_password_dialog.open_dialog()

    def open_dialog(self):
        self.soundboard_switch.value = self.party_mode_settings.is_party_mode()
        self.soundboard_switch.update()
        self.open = True
        self.update()

    def close_dialog(self):
        self.open = False
        self.update()
