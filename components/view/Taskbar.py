import flet as ft

from components.dialogs.AudioEffectsDialog import AudioEffectsDialog
from components.dialogs.SettingsShutdownDialog import SettingsShutdownDialog
from components.dialogs.VolumeDialog import VolumeDialog
from components.dialogs.WifiConnectionDialog import WifiConnectionDialog
from components.dialogs.WifiDialog import WifiDialog
from helper.Audio import Audio
from helper.AudioEffects import AudioEffects
from helper.BluetoothHelper import BluetoothHelper
from helper.Constants import Constants
from helper.PageState import PageState
from helper.ThemeHelper import ThemeHelper
from helper.WifiHelper import WifiHelper

audio_helper = Audio()
audio_effects = AudioEffects()
wifi_helper = WifiHelper()
bluetooth_helper = BluetoothHelper()
theme_helper = ThemeHelper()


class Taskbar(ft.AppBar):
    wifi_connection_dialog: WifiConnectionDialog = None
    wifi_dialog: WifiDialog = None

    taskbar_icon_size = 28

    ico_shutdown = ft.IconButton(
        icon=ft.Icons.POWER_SETTINGS_NEW,
        icon_size=taskbar_icon_size,
    )

    ico_toggle_theme = ft.IconButton(
        icon=(
            ft.Icons.LIGHT_MODE
            if theme_helper.get_theme() == ft.ThemeMode.LIGHT
            else ft.Icons.DARK_MODE
        ),
        icon_size=taskbar_icon_size,
    )

    ico_wifi = ft.IconButton(icon=ft.Icons.WIFI, icon_size=taskbar_icon_size)
    ico_bluetooth = ft.Icon(name=ft.Icons.BLUETOOTH, size=taskbar_icon_size)

    ico_volume = ft.Icon(name=ft.Icons.VOLUME_UP_ROUNDED, size=taskbar_icon_size)
    txt_volume = ft.Text(f"{audio_helper.get_volume()}%", size=18)

    ico_bass = ft.Icon(name=ft.Icons.SURROUND_SOUND, size=taskbar_icon_size)
    txt_bass = ft.Text(f"{Constants.current_bass_step}", size=18)

    ico_treble = ft.Icon(name=ft.Icons.HEIGHT, size=taskbar_icon_size)
    txt_treble = ft.Text(f"{Constants.current_treble_step}", size=18)

    def __init__(self, on_volume_update, on_mute_update, on_bass_update):
        super().__init__()

        self.on_bass_update = on_bass_update

        self.volume_dialog = VolumeDialog(
            on_update=self.update_volume_icon,
            on_volume_update=on_volume_update,
            on_mute_update=on_mute_update,
        )
        self.audio_effects_dialog = AudioEffectsDialog(
            on_update_bass=self.bass_update,
            on_update_treble=self.update_treble_icon,
        )
        self.shutdown_dialog = SettingsShutdownDialog()

        PageState.page.add(self.volume_dialog)
        PageState.page.add(self.audio_effects_dialog)
        PageState.page.add(self.shutdown_dialog)

        self.title = ft.Row(
            controls=[
                ft.Container(
                    content=ft.Row([self.ico_volume, self.txt_volume]),
                    on_click=lambda e: self.volume_dialog.open_dialog(),
                ),
                ft.Container(
                    content=ft.Row([self.ico_bass, self.txt_bass]),
                    on_click=lambda e: self.audio_effects_dialog.open_dialog(),
                ),
                ft.Container(
                    content=ft.Row([self.ico_treble, self.txt_treble]),
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
        self.wifi_dialog = WifiDialog(self.wifi_connection_dialog, self.update_wifi)

        self.ico_wifi.on_click = lambda e: self.wifi_dialog.open_dialog()
        self.ico_toggle_theme.on_click = lambda e: self.toggle_theme()
        self.ico_shutdown.on_click = lambda e: self.open_shutdown_dialog()

        PageState.page.add(self.wifi_connection_dialog)
        PageState.page.add(self.wifi_dialog)

    def update(self):
        self.update_volume_icon()
        self.volume_dialog.update_content()
        self.update_bass_icon()
        self.update_treble_icon()
        self.audio_effects_dialog.update_content()
        self.update_wifi()
        self.update_bluetooth_icon()
        super().update()

    def toggle_theme(self):
        theme_helper.toggle_theme()
        self.ico_toggle_theme.icon = (
            ft.Icons.LIGHT_MODE
            if theme_helper.get_theme() == ft.ThemeMode.LIGHT
            else ft.Icons.DARK_MODE
        )
        self.ico_toggle_theme.update()
        PageState.page.theme_mode = theme_helper.get_theme()
        PageState.page.update()

    def update_wifi(self):
        self.ico_wifi.icon = ft.Icons.WIFI
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
            ft.Icons.VOLUME_OFF_ROUNDED if audio_helper.is_mute() else ft.Icons.VOLUME_UP_ROUNDED
        )
        self.ico_volume.color = ft.Colors.RED if audio_helper.is_mute() else ft.Colors.ON_SURFACE
        self.ico_volume.update()
        self.txt_volume.value = (
            f"{audio_helper.get_volume()}%" if not audio_helper.is_mute() else ""
        )
        self.txt_volume.update()

    def bass_update(self):
        self.update_bass_icon()
        self.on_bass_update(Constants.current_bass_step)

    def update_bass_icon(self):
        self.txt_bass.value = Constants.current_bass_step
        self.txt_bass.update()

    def update_treble_icon(self):
        self.txt_treble.value = Constants.current_treble_step
        self.txt_treble.update()

    def open_shutdown_dialog(self):
        self.shutdown_dialog.open_dialog()
