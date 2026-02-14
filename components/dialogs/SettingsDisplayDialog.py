import flet as ft

from components.dialogs.SplashscreenDialog import SplashscreenDialog
from components.dialogs.UpdatesRestartDialog import UpdatesRestartDialog
from core.settings.factories.scrollbar import create_scrollbar_settings
from helper.PageState import PageState
from helper.SystemHelper import SystemHelper

system_helper = SystemHelper()


class SettingsDisplayDialog(ft.AlertDialog):
    def __init__(self):
        super().__init__()
        self.updates_restart_dialog = UpdatesRestartDialog()
        self.splashscreen_dialog = SplashscreenDialog(self)

        self.scrollbar_settings = create_scrollbar_settings()

        PageState.page.add(self.updates_restart_dialog)
        PageState.page.add(self.splashscreen_dialog)

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
                    value=self.scrollbar_settings.is_scrollbar_enabled(),
                ),
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
        self.scrollbar_settings.toggle_scrollbar_enabled()
        self.close_dialog()
        self.updates_restart_dialog.open_dialog()

    def slider_changed(self, e):
        system_helper.change_screen_brightness(e.control.value)

    def open_splashscreen_dialog(self):
        self.splashscreen_dialog.open_dialog()

    def open_dialog(self):
        self.open = True
        self.update()

    def close_dialog(self):
        self.open = False
        self.update()
