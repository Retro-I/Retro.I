import flet as ft

from components.dialogs.SettingsAppControlDialog import SettingsAppControlDialog
from components.dialogs.SettingsCreditsDialog import SettingsCreditsDialog
from components.dialogs.SettingsDisplayDialog import SettingsDisplayDialog
from components.dialogs.SettingsFavoriteStationDialog import SettingsFavoriteStationDialog
from components.dialogs.SettingsInfoDialog import SettingsInfoDialog
from components.dialogs.SettingsLedDialog import SettingsLedDialog
from components.dialogs.SettingsShutdownDialog import SettingsShutdownDialog
from components.dialogs.SettingsUpdateDialog import SettingsUpdateDialog
from components.Scrollbar import with_scrollbar_space
from components.SettingsButton import SettingsButton
from helper.PageState import PageState
from helper.Sounds import Sounds

sounds = Sounds()


class SettingsTab(ft.Column):
    def __init__(self):
        super().__init__()

        self.shutdown_dialog = SettingsShutdownDialog()
        self.app_control_dialog = SettingsAppControlDialog()
        self.display_dialog = SettingsDisplayDialog()
        self.led_dialog = SettingsLedDialog()
        self.favorite_station_dialog = SettingsFavoriteStationDialog()
        self.info_dialog = SettingsInfoDialog()
        self.credits_dialog = SettingsCreditsDialog()
        self.update_dialog = SettingsUpdateDialog()

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
                            ft.icons.POWER_SETTINGS_NEW,
                            "Ausschalten",
                            lambda e: self.shutdown_dialog.open_dialog(),
                        ),
                        SettingsButton(
                            ft.icons.EXIT_TO_APP,
                            "App",
                            lambda e: self.app_control_dialog.open_dialog(),
                        ),
                        SettingsButton(
                            ft.icons.DISPLAY_SETTINGS,
                            "Anzeige",
                            lambda e: self.display_dialog.open_dialog(),
                        ),
                        SettingsButton(
                            ft.icons.COLOR_LENS,
                            "LED-Streifen",
                            lambda e: self.led_dialog.open_dialog(),
                        ),
                        SettingsButton(
                            ft.icons.FAVORITE,
                            "Autoplay",
                            lambda e: self.favorite_station_dialog.open_dialog(),
                        ),
                        SettingsButton(
                            ft.icons.INFO, "Info", lambda e: self.info_dialog.open_dialog()
                        ),
                        SettingsButton(
                            ft.icons.FILE_DOWNLOAD_OUTLINED,
                            "Updates",
                            lambda e: self.update_dialog.open_dialog(),
                        ),
                        SettingsButton(
                            ft.icons.STAR,
                            "Credits",
                            lambda e: self.credits_dialog.open_dialog(),
                        ),
                    ],
                ),
            ),
        ]

        PageState.page.add(self.shutdown_dialog)
        PageState.page.add(self.app_control_dialog)
        PageState.page.add(self.display_dialog)
        PageState.page.add(self.led_dialog)
        PageState.page.add(self.favorite_station_dialog)
        PageState.page.add(self.info_dialog)
        PageState.page.add(self.update_dialog)
        PageState.page.add(self.credits_dialog)

    def show(self):
        self.visible = True
        self.update()

    def hide(self):
        self.visible = False
        self.update()
