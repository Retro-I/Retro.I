import flet as ft

from components.dialogs.SettingsShutdownDialog import SettingsShutdownDialog
from components.dialogs.VolumeDialog import VolumeDialog
from components.dialogs.WifiConnectionDialog import WifiConnectionDialog
from components.dialogs.WifiDialog import WifiDialog
from helper.Audio import Audio
from helper.AudioEffects import AudioEffects
from helper.BluetoothHelper import BluetoothHelper
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

    ico_wifi = ft.IconButton(
        icon=ft.Icons.WIFI, icon_size=taskbar_icon_size, icon_color=ft.Colors.GREEN
    )
    ico_bluetooth = ft.Icon(name=ft.Icons.BLUETOOTH, size=taskbar_icon_size)

    ico_volume = ft.Icon(name=ft.Icons.VOLUME_UP_ROUNDED, size=taskbar_icon_size)
    txt_volume = ft.Text(f"{audio_helper.get_volume()}%", size=18)

    ico_bass = ft.Icon(name=ft.Icons.SURROUND_SOUND, size=taskbar_icon_size)
    txt_bass = ft.Text(f"{audio_effects.get_bass_value()} dB", size=18)

    ico_pitch = ft.Icon(name=ft.Icons.HEIGHT, size=taskbar_icon_size)
    txt_pitch = ft.Text(audio_effects.get_pitch_value(), size=18)

    def __init__(self, on_volume_update, on_mute_update):
        super().__init__()

        self.volume_dialog = VolumeDialog(
            on_update=self.update_volume_icon,
            on_volume_update=on_volume_update,
            on_mute_update=on_mute_update,
        )
        self.shutdown_dialog = SettingsShutdownDialog()

        PageState.page.add(self.volume_dialog)
        PageState.page.add(self.shutdown_dialog)

        self.leading = ft.Row(
            [
                ft.Container(
                    content=ft.Row([self.ico_volume, self.txt_volume]),
                    on_click=lambda e: self.volume_dialog.open_dialog(),
                ),
                ft.VerticalDivider(),
                ft.Row([self.ico_bass, self.txt_bass]),
                ft.VerticalDivider(),
                ft.Row([self.ico_pitch, self.txt_pitch]),
                ft.VerticalDivider(),
            ]
        )
        self.title = ft.Text("Retro.I")
        self.center_title = True
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
        self.wifi_dialog = WifiDialog(self.wifi_connection_dialog)

        self.ico_wifi.on_click = lambda e: self.wifi_dialog.open_dialog()
        self.ico_toggle_theme.on_click = lambda e: self.toggle_theme()
        self.ico_shutdown.on_click = lambda e: self.open_shutdown_dialog()

        PageState.page.add(self.wifi_connection_dialog)
        PageState.page.add(self.wifi_dialog)

    def update(self):
        self.update_volume_icon()
        self.volume_dialog.update_content()
        self.update_bass()
        self.update_pitch()
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
        self.ico_wifi.icon = (
            ft.Icons.WIFI if wifi_helper.is_connected() else ft.Icons.WIFI_OFF_ROUNDED
        )
        self.ico_wifi.color = (
            ft.Colors.GREEN if wifi_helper.is_connected() else ft.Colors.ON_SURFACE
        )
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

    def update_bass(self):
        self.txt_bass.value = (
            f"+{audio_effects.get_bass_value()} dB"
            if audio_effects.get_bass_value() > 0
            else f"{audio_effects.get_bass_value()} dB"
        )
        self.txt_bass.update()

    def update_pitch(self):
        self.txt_pitch.value = audio_effects.get_pitch_value()
        self.txt_pitch.update()

    def open_shutdown_dialog(self):
        self.shutdown_dialog.open_dialog()
