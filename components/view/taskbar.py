import flet as ft

from components.dialogs.audio_effects_dialog import AudioEffectsDialog
from components.dialogs.settings_shutdown_dialog import SettingsShutdownDialog
from components.dialogs.volume_dialog import VolumeDialog
from components.dialogs.wifi_connection_dialog import WifiConnectionDialog
from components.dialogs.wifi_dialog import WifiDialog
from core.helper_factories import (
    create_audio_helper,
    create_system_helper,
    create_theme_helper,
)
from helper.audio_effects import AudioEffects
from helper.bluetooth_helper import BluetoothHelper
from helper.constants import Constants
from helper.page_state import PageState
from helper.wifi_helper import WifiHelper

audio_helper = create_audio_helper()
audio_effects = AudioEffects()
wifi_helper = WifiHelper()
bluetooth_helper = BluetoothHelper()


class Taskbar(ft.AppBar):
    wifi_connection_dialog: WifiConnectionDialog = None
    wifi_dialog: WifiDialog = None

    taskbar_icon_size = 28

    def __init__(self, on_bass_update, on_treble_update):
        super().__init__()
        self.theme_helper = create_theme_helper()
        self.system_helper = create_system_helper()

        self.on_bass_update = on_bass_update
        self.on_treble_update = on_treble_update

        self.volume_dialog = VolumeDialog()
        self.audio_effects_dialog = AudioEffectsDialog()
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
                if self.system_helper.is_connection_over_wifi()
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
        self.txt_volume = ft.Text(f"{audio_helper.get_volume()}%", size=18)

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
        self.volume_dialog.update_content()
        self.update_eq_icon()
        self.audio_effects_dialog.update_content()
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
        if self.system_helper.is_connection_over_lan():
            self.ico_wifi.icon = ft.Icons.LAN
            self.ico_wifi.icon_color = ft.Colors.GREEN
            self.ico_wifi.update()
            return

        if self.system_helper.is_connection_over_wifi():
            self.ico_wifi.icon = ft.Icons.WIFI
            self.ico_wifi.icon_color = ft.Colors.GREEN
            self.ico_wifi.update()

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
            if audio_helper.is_mute()
            else ft.Icons.VOLUME_UP_ROUNDED
        )
        self.ico_volume.color = (
            ft.Colors.RED if audio_helper.is_mute() else ft.Colors.ON_SURFACE
        )
        self.ico_volume.update()
        self.txt_volume.value = (
            f"{audio_helper.get_volume()}%"
            if not audio_helper.is_mute()
            else ""
        )
        self.txt_volume.update()

    def bass_update(self):
        self.update_eq_icon()
        self.on_bass_update(Constants.current_bass_step)

    def treble_update(self):
        self.update_eq_icon()
        self.on_treble_update(Constants.current_treble_step)

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
        if (
            self.system_helper.is_connection_over_wifi()
            or self.system_helper.get_current_ssid() == ""
        ) and not self.system_helper.is_connection_over_lan():
            self.wifi_dialog.open_dialog()
