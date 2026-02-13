import threading
import time

import flet as ft

from components.dialogs.StartupErrorDialog import StartupErrorDialog
from components.GpioButton import GpioButton
from components.RotaryBass import RotaryBass
from components.RotaryTreble import RotaryTreble
from components.RotaryVolume import RotaryVolume
from components.view.Taskbar import Taskbar
from components.view.Theme import Theme
from core.app_platform import AppPlatform, get_app_platform
from core.app_state import AppState
from helper.Audio import Audio
from helper.AudioEffects import AudioEffects
from helper.BluetoothHelper import BluetoothHelper
from helper.Constants import Constants
from helper.GpioHelper import GpioHelper
from helper.LogsHelper import LogsHelper
from helper.PageState import PageState
from helper.RadioHelper import RadioHelper
from helper.SettingsSyncHelper import SettingsSyncHelper
from helper.Sounds import Sounds
from helper.StartupErrorHelper import StartupErrorHelper
from helper.Stations import Stations
from helper.Strip import Strip
from helper.SystemHelper import SystemHelper
from helper.ThemeHelper import ThemeHelper
from helper.WifiHelper import WifiHelper

wifi_helper = WifiHelper()
radio_helper = RadioHelper()
bluetooth_helper = BluetoothHelper()
system_helper = SystemHelper()
startup_error_helper = StartupErrorHelper()
settings_sync_helper = SettingsSyncHelper()
stations_helper = Stations()
constants = Constants()
sounds = Sounds()
audio_helper = Audio()
page_helper = PageState()
audio_effects = AudioEffects()
theme_helper = ThemeHelper()
gpio_helper = GpioHelper()
logs_helper = LogsHelper()


def on_error(e):
    startup_error_helper.write_startup_error(e)
    system_helper.change_revision("main")
    system_helper.restart_app()


def init():
    settings_sync_helper.validate_and_repair_all_settings()
    audio_helper.init_sound()
    logs_helper.print_debug_infos()


def main(page: ft.Page):
    init()

    AppState()

    page.on_error = on_error
    page.theme_mode = theme_helper.get_theme()
    page.update()

    PageState.page = page

    bluetooth_helper.on_startup()

    Strip()
    taskbar = Taskbar()
    theme = Theme()

    page.navigation_bar = theme.navbar
    page.appbar = taskbar
    page.window.maximized = True
    page.window.frameless = True
    page.spacing = 0
    page.theme = theme.get()
    page.dark_theme = theme.get()
    page.title = "Retro.I"

    button = GpioButton(21, audio_helper.play_toast)
    button.activate()

    shutdown_button = GpioButton(
        gpio_helper.shutdown_button(), system_helper.shutdown_system
    )
    shutdown_button.activate()

    for item in theme.get_tabs():
        page.add(item)

    theme.radio_tab.radio_grid.reload()

    if startup_error_helper.is_startup_error():
        startup_error_dialog = StartupErrorDialog()
        page.add(startup_error_dialog)
        # startup_error_dialog.open_dialog()

    page.update()

    if get_app_platform() == AppPlatform.PI:
        RotaryVolume()
        RotaryBass()
        RotaryTreble()

        audio_helper.startup_sound()
        audio_effects.start()

    page.on_error = None

    def background_processes():
        while True:
            theme.radio_tab.song_info_row.reload()
            AppState.app_state.update_taskbar()
            time.sleep(2)

    process = threading.Thread(target=background_processes)
    process.start()

    if (
        audio_helper.is_default_station_autoplay_enabled()
        and stations_helper.get_favorite_station() is not None
    ):
        theme.radio_tab.radio_grid.change_radio_station(
            station=stations_helper.get_favorite_station(),
            index=stations_helper.load_radio_stations().index(
                stations_helper.get_favorite_station()
            ),
        )


try:
    ft.app(main, assets_dir="assets")
except Exception as e:
    on_error(e)
