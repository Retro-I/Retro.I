import logging
import threading
import time

import flet as ft

from components.dialogs.startup_error_dialog import StartupErrorDialog
from components.gpio_button import GpioButton
from components.rotary_bass import RotaryBass
from components.rotary_treble import RotaryTreble
from components.rotary_volume import RotaryVolume
from components.view.taskbar import Taskbar
from components.view.theme import Theme
from core.app_state import AppState
from core.factories.helper_factories import (
    create_audio_helper,
    create_player_helper,
    create_settings_sync_helper,
    create_sounds_helper,
    create_strip_state,
    create_system_helper,
    create_theme_helper,
)
from core.factories.settings_factories import (
    create_gpio_settings,
    create_radio_stations_settings,
)
from helper.audio_effects import AudioEffects
from helper.bluetooth_helper import BluetoothHelper
from helper.constants import Constants
from helper.logs_helper import LogsHelper
from helper.page_state import PageState
from helper.radio_helper import RadioHelper
from helper.startup_error_helper import StartupErrorHelper
from helper.wifi_helper import WifiHelper

logger = logging.getLogger(__name__)

wifi_helper = WifiHelper()
radio_helper = RadioHelper()
bluetooth_helper = BluetoothHelper()
system_helper = create_system_helper()
startup_error_helper = StartupErrorHelper()
settings_sync_helper = create_settings_sync_helper()
stations_helper = create_radio_stations_settings()
constants = Constants()
sounds = create_sounds_helper()
audio_helper = create_audio_helper()
page_helper = PageState()
audio_effects = AudioEffects()
theme_helper = create_theme_helper()
gpio_helper = create_gpio_settings()
logs_helper = LogsHelper()
player = create_player_helper()


def on_error(e):
    startup_error_helper.write_startup_error(e)
    system_helper.change_revision("main")
    system_helper.restart_app()


def init():
    settings_sync_helper.validate_and_repair_all_settings()
    audio_helper.init_sound()
    logs_helper.print_debug_infos()
    AppState()


def main(page: ft.Page):
    try:
        init()
    except Exception as ex:
        logger.info(ex)

    page.theme_mode = theme_helper.get_theme()
    page.update()

    PageState.page = page

    bluetooth_helper.on_startup()

    strip = create_strip_state()
    taskbar = Taskbar(
        on_bass_update=strip.update_bass_strip,
        on_treble_update=strip.update_treble_strip,
    )
    theme = Theme(taskbar, strip)

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

    RotaryVolume()
    RotaryBass()
    RotaryTreble()

    def background_processes():
        while True:
            theme.radio_tab.song_info_row.reload()
            taskbar.update()
            time.sleep(2)

    process = threading.Thread(target=background_processes)
    process.start()

    player.startup_sound()
    audio_effects.start()

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


ft.app(main, assets_dir="assets")
