import flet as ft

from components.dialogs.AdminPasswordDialog import AdminPasswordDialog
from components.dialogs.SplashscreenDialog import SplashscreenDialog
from components.dialogs.UpdatesRestartDialog import UpdatesRestartDialog
from helper.PageState import PageState
from helper.PartyModeHelper import PartyModeHelper
from helper.ScrollbarSettingsHelper import ScrollbarSettingsHelper
from helper.SystemHelper import SystemHelper

system_helper = SystemHelper()
scrollbar_settings_helper = ScrollbarSettingsHelper()
party_mode_helper = PartyModeHelper()


class SettingsDisplayDialog(ft.AlertDialog):
    def __init__(self):
        super().__init__()
        self.updates_restart_dialog = UpdatesRestartDialog()
        self.splashscreen_dialog = SplashscreenDialog(self)
        self.admin_password_dialog = AdminPasswordDialog(
            self.updates_restart_dialog.open_dialog
        )

        PageState.page.add(self.updates_restart_dialog)
        PageState.page.add(self.splashscreen_dialog)
        PageState.page.add(self.admin_password_dialog)

        self.soundboard_switch = ft.Switch(
            "Soundboard anzeigen (Neustart erforderlich!)",
            label_style=ft.TextStyle(size=18),
            on_change=lambda e: self.open_admin_password_dialog(),
            value=party_mode_helper.is_party_mode(),
        )

        self.title = ft.Text("Anzeige")
        self.content = ft.Column(
            alignment=ft.MainAxisAlignment.CENTER,
            width=500,
            tight=True,
            controls=[
                ft.Switch(
                    "Scrollbar anzeigen (Neustart erforderlich!)",
                    label_style=ft.TextStyle(size=18),
                    on_change=lambda e: self.toggle_enable_scrollbar(),
                    value=scrollbar_settings_helper.is_scrollbar_enabled(),
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
                            value=system_helper.get_curr_brightness(),
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
        scrollbar_settings_helper.toggle_scrollbar_enabled()
        self.close_dialog()
        self.updates_restart_dialog.open_dialog()

    def slider_changed(self, e):
        system_helper.change_screen_brightness(e.control.value)

    def open_splashscreen_dialog(self):
        self.splashscreen_dialog.open_dialog()

    def open_admin_password_dialog(self):
        self.admin_password_dialog.open_dialog()

    def open_dialog(self):
        self.soundboard_switch.value = party_mode_helper.is_party_mode()
        self.soundboard_switch.update()
        self.open = True
        self.update()

    def close_dialog(self):
        self.open = False
        self.update()
