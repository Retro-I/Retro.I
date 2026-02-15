import flet as ft

from components.dialogs.AudioEffectsDialog import AudioEffectsDialog
from components.dialogs.SettingsShutdownDialog import SettingsShutdownDialog
from components.dialogs.VolumeDialog import VolumeDialog
from components.dialogs.WifiConnectionDialog import WifiConnectionDialog
from components.dialogs.WifiDialog import WifiDialog
from core.app_state import AppState
from core.factories.strip_factory import create_strip_state
from core.helpers.factories.audio import create_audio_helper
from core.helpers.factories.system import create_system_helper
from core.helpers.factories.theme import create_theme_helper
from helper.AudioEffects import AudioEffects
from helper.BluetoothHelper import BluetoothHelper
from helper.Constants import Constants
from helper.PageState import PageState
from helper.WifiHelper import WifiHelper

audio_effects = AudioEffects()
wifi_helper = WifiHelper()
bluetooth_helper = BluetoothHelper()


class Taskbar(ft.AppBar):
    wifi_connection_dialog: WifiConnectionDialog = None
    wifi_dialog: WifiDialog = None

    taskbar_icon_size = 28

    def __init__(self):
        super().__init__()
        AppState.app_state.subscribe(self.update)
        self.strip_state = create_strip_state()
        self.audio_state = create_audio_helper()

        self.system_helper = create_system_helper()
        self.theme_helper = create_theme_helper()

        self.audio_effects_dialog = AudioEffectsDialog()
        self.volume_dialog = VolumeDialog()
        self.shutdown_dialog = SettingsShutdownDialog()

        PageState.page.add(self.volume_dialog)
        PageState.page.add(self.audio_effects_dialog)
        PageState.page.add(self.shutdown_dialog)

        self.ico_shutdown = ft.IconButton(
            icon=ft.Icons.POWER_SETTINGS_NEW,
            icon_size=self.taskbar_icon_size,
            on_click=lambda e: self.on_ico_shutdown_click(),
        )

        self.ico_toggle_theme = ft.IconButton(
            icon=(
                ft.Icons.LIGHT_MODE
                if self.theme_helper.get_theme() == ft.ThemeMode.LIGHT
                else ft.Icons.DARK_MODE
            ),
            icon_size=self.taskbar_icon_size,
            on_click=lambda e: self.on_ico_toggle_theme_click(),
        )

        self.ico_wifi = ft.IconButton(
            icon=(
                ft.Icons.WIFI
                if self.system_helper.get_current_ssid() != ""
                else ft.Icons.LAN
            ),
            icon_size=self.taskbar_icon_size,
            on_click=lambda e: self.on_ico_wifi_click(),
        )
        self.ico_bluetooth = ft.Icon(
            name=ft.Icons.BLUETOOTH,
            size=self.taskbar_icon_size,
        )

        self.ico_volume = ft.Icon(
            name=ft.Icons.VOLUME_UP_ROUNDED, size=self.taskbar_icon_size
        )
        self.txt_volume = ft.Text(f"{self.audio_state.get_volume()}%", size=18)

        self.ico_eq = ft.Icon(
            name=ft.Icons.EQUALIZER, size=self.taskbar_icon_size
        )
        self.txt_eq = ft.Text(
            f"Bass: {Constants.current_bass_step}  |  "
            f"Treble: {Constants.current_treble_step}",
            size=18,
        )

        self.title = ft.Row(
            controls=[
                ft.Container(
                    content=ft.Row(
                        [
                            self.ico_volume,
                            self.txt_volume,
                            ft.VerticalDivider(),
                        ]
                    ),
                    on_click=lambda e: self.volume_dialog.open_dialog(),
                ),
                ft.Container(
                    content=ft.Row(
                        [
                            self.ico_eq,
                            self.txt_eq,
                            ft.VerticalDivider(),
                        ]
                    ),
                    on_click=lambda e: self.audio_effects_dialog.open_dialog(),
                ),
            ]
        )
        self.bgcolor = ft.Colors.SURFACE_CONTAINER_HIGHEST
        self.toolbar_height = 50
        self.actions = [
            ft.Row(
                controls=[
                    ft.VerticalDivider(),
                    self.ico_shutdown,
                    ft.VerticalDivider(),
                    self.ico_toggle_theme,
                    ft.VerticalDivider(),
                    self.ico_wifi,
                    ft.VerticalDivider(),
                    self.ico_bluetooth,
                    ft.VerticalDivider(),
                ],
                spacing=10,
            )
        ]

        self.wifi_connection_dialog = WifiConnectionDialog(self.update)
        self.wifi_dialog = WifiDialog(
            self.wifi_connection_dialog, self.update_wifi
        )

        PageState.page.add(self.wifi_connection_dialog)
        PageState.page.add(self.wifi_dialog)

    def update(self):
        self.update_volume_icon()
        self.update_eq_icon()
        self.update_wifi()
        self.update_bluetooth_icon()
        super().update()

    def toggle_theme(self):
        self.theme_helper.toggle_theme()
        self.ico_toggle_theme.icon = (
            ft.Icons.LIGHT_MODE
            if self.theme_helper.get_theme() == ft.ThemeMode.LIGHT
            else ft.Icons.DARK_MODE
        )
        self.ico_toggle_theme.update()
        PageState.page.theme_mode = self.theme_helper.get_theme()
        PageState.page.update()

    def update_wifi(self):
        self.ico_wifi.icon = (
            ft.Icons.WIFI
            if self.system_helper.get_current_ssid() != ""
            else ft.Icons.LAN
        )
        self.ico_wifi.icon_color = ft.Colors.GREEN

        if not wifi_helper.is_enabled():
            self.ico_wifi.icon = ft.Icons.WIFI_OFF
            self.ico_wifi.icon_color = ft.Colors.ON_SURFACE
            self.ico_wifi.update()
            return

        if not wifi_helper.is_connected():
            self.ico_wifi.icon = ft.Icons.WIFI_FIND
            self.ico_wifi.icon_color = ft.Colors.ON_SURFACE
            self.ico_wifi.update()
            return

        self.ico_wifi.update()

    def update_bluetooth_icon(self):
        if bluetooth_helper.is_bluetooth_on():
            self.ico_bluetooth.name = ft.Icons.BLUETOOTH_ROUNDED
            self.ico_bluetooth.color = ft.Colors.ON_SURFACE

            if bluetooth_helper.is_discovery_on():
                self.ico_bluetooth.color = ft.Colors.GREEN
            else:
                self.ico_bluetooth.color = ft.Colors.ON_SURFACE

        else:
            self.ico_bluetooth.name = ft.Icons.BLUETOOTH_DISABLED_ROUNDED
            self.ico_bluetooth.color = ft.Colors.ON_SURFACE

        if bluetooth_helper.is_connected():
            self.ico_bluetooth.name = ft.Icons.BLUETOOTH_CONNECTED_ROUNDED
            self.ico_bluetooth.color = ft.Colors.GREEN

        self.ico_bluetooth.update()

    def update_volume_icon(self):
        self.ico_volume.name = (
            ft.Icons.VOLUME_OFF_ROUNDED
            if self.audio_state.is_mute()
            else ft.Icons.VOLUME_UP_ROUNDED
        )
        self.ico_volume.color = (
            ft.Colors.RED
            if self.audio_state.is_mute()
            else ft.Colors.ON_SURFACE
        )
        self.ico_volume.update()
        self.txt_volume.value = (
            f"{self.audio_state.get_volume()}%"
            if not self.audio_state.is_mute()
            else ""
        )
        self.txt_volume.update()

    def bass_update(self):
        self.update_eq_icon()
        self.strip_state.update_bass_strip(Constants.current_bass_step)

    def treble_update(self):
        self.update_eq_icon()
        self.strip_state.update_treble_strip(Constants.current_treble_step)

    def update_eq_icon(self):
        self.txt_eq.value = (
            f"Bass: {Constants.current_bass_step}  |  "
            f"Treble: {Constants.current_treble_step}"
        )
        self.txt_eq.update()

    def on_ico_shutdown_click(self):
        self.shutdown_dialog.open_dialog()

    def on_ico_toggle_theme_click(self):
        self.toggle_theme()

    def on_ico_wifi_click(self):
        if self.system_helper.get_current_ssid() != "":
            self.wifi_dialog.open_dialog()
