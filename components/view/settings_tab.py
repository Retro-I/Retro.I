import flet as ft

from components.dialogs.settings_app_control_dialog import (
    SettingsAppControlDialog,
)
from components.dialogs.settings_audio_dialog import SettingsAudioDialog
from components.dialogs.settings_developer_mode_dialog import (
    SettingsDeveloperModeDialog,
)
from components.dialogs.settings_display_dialog import SettingsDisplayDialog
from components.dialogs.settings_info_dialog import SettingsInfoDialog
from components.dialogs.settings_led_dialog import SettingsLedDialog
from components.dialogs.settings_logs_dialog import SettingsLogsDialog
from components.dialogs.settings_shutdown_dialog import SettingsShutdownDialog
from components.dialogs.settings_update_dialog import SettingsUpdateDialog
from components.scrollbar import with_scrollbar_space
from components.settings_button import SettingsButton
from core.factories.settings_factories import (
    create_developer_mode_settings as developer_settings,
)
from helper.page_state import PageState


class SettingsTab(ft.Column):
    def __init__(self, strip):
        super().__init__()

        self.shutdown_dialog = SettingsShutdownDialog()
        self.app_control_dialog = SettingsAppControlDialog()
        self.audio_dialog = SettingsAudioDialog()
        self.display_dialog = SettingsDisplayDialog()
        self.led_dialog = SettingsLedDialog(strip)
        self.info_dialog = SettingsInfoDialog()
        self.update_dialog = SettingsUpdateDialog()
        self.logs_dialog = SettingsLogsDialog()
        self.developer_mode_dialog = SettingsDeveloperModeDialog()

        self.visible = False
        self.expand = True
        self.controls = [
            ft.Text("Einstellungen", size=24, weight=ft.FontWeight.BOLD),
            with_scrollbar_space(
                ft.GridView(
                    expand=True,
                    runs_count=5,
                    max_extent=150,
                    child_aspect_ratio=1.0,
                    spacing=20,
                    run_spacing=50,
                    controls=[
                        SettingsButton(
                            ft.Icons.EXIT_TO_APP,
                            text="App",
                            callback=(
                                lambda e: self.app_control_dialog.open_dialog()
                            ),
                            visible=(
                                developer_settings().is_developer_mode_active()
                            ),
                        ),
                        SettingsButton(
                            ft.Icons.AUDIOTRACK,
                            text="Audio",
                            callback=lambda e: self.audio_dialog.open_dialog(),
                        ),
                        SettingsButton(
                            ft.Icons.DISPLAY_SETTINGS,
                            text="Anzeige",
                            callback=lambda e: (
                                self.display_dialog.open_dialog()
                            ),
                        ),
                        SettingsButton(
                            ft.Icons.COLOR_LENS,
                            text="LED-Streifen",
                            callback=lambda e: self.led_dialog.open_dialog(),
                        ),
                        SettingsButton(
                            ft.Icons.INFO_OUTLINED,
                            text="Info's",
                            callback=lambda e: self.info_dialog.open_dialog(),
                        ),
                        SettingsButton(
                            ft.Icons.BROWSER_UPDATED,
                            text="Updates",
                            callback=lambda e: self.update_dialog.open_dialog(),
                            visible=(
                                developer_settings().is_developer_mode_active()
                            ),
                        ),
                        SettingsButton(
                            ft.Icons.NOTES,
                            text="Logs",
                            callback=lambda e: self.logs_dialog.open_dialog(),
                            visible=(
                                developer_settings().is_developer_mode_active()
                            ),
                        ),
                        SettingsButton(
                            ft.Icons.BUILD,
                            text="Entwickler",
                            callback=lambda e: (
                                self.developer_mode_dialog.open_dialog()
                            ),
                        ),
                    ],
                ),
            ),
        ]
        PageState.page.add(self.shutdown_dialog)
        PageState.page.add(self.app_control_dialog)
        PageState.page.add(self.audio_dialog)
        PageState.page.add(self.display_dialog)
        PageState.page.add(self.led_dialog)
        PageState.page.add(self.info_dialog)
        PageState.page.add(self.update_dialog)
        PageState.page.add(self.logs_dialog)
        PageState.page.add(self.developer_mode_dialog)

    def show(self):
        self.visible = True
        self.update()

    def hide(self):
        self.visible = False
        self.update()
