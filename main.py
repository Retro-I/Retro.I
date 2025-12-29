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
from helper.Audio import Audio
from helper.AudioEffects import AudioEffects
from helper.BluetoothHelper import BluetoothHelper
from helper.Constants import Constants
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


def on_error(e):
    startup_error_helper.write_startup_error(e)
    system_helper.change_revision("main")
    system_helper.restart_app()


def init():
    settings_sync_helper.validate_and_repair_all_settings()
    audio_helper.init_sound()


def main(page: ft.Page):
    init()

    page.on_error = on_error
    page.theme_mode = theme_helper.get_theme()
    page.update()

    start = time.time()
    PageState.page = page

    bluetooth_helper.on_startup()

    strip = Strip()
    taskbar = Taskbar(
        on_volume_update=strip.update_sound_strip,
        on_mute_update=strip.toggle_mute,
        on_bass_update=strip.update_bass_strip,
        on_treble_update=strip.update_treble_strip,
    )
    theme = Theme(taskbar, strip.update_strip)

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

    for item in theme.get_tabs():
        page.add(item)

    theme.radio_tab.radio_grid.reload()

    if startup_error_helper.startup_error() is not None:
        startup_error_dialog = StartupErrorDialog()
        page.add(startup_error_dialog)
        startup_error_dialog.open_dialog()

        startup_error_helper.reset_startup_error()

    page.update()

    RotaryVolume(
        on_taskbar_update=taskbar.update,
        on_strip_toggle_mute=strip.toggle_mute,
        on_strip_update_sound=strip.update_sound_strip,
    )
    RotaryBass(on_taskbar_update=taskbar.update, on_bass_update=strip.update_bass_strip)
    RotaryTreble(on_taskbar_update=taskbar.update, on_treble_update=strip.update_treble_strip)

    audio_helper.startup_sound()
    audio_effects.start()

    end = time.time()

    page.on_error = None

    print(f"Startup took: {end-start}")

    def background_processes():
        while True:
            theme.radio_tab.song_info_row.reload()
            taskbar.update()
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
