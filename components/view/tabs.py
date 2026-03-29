import time

from components.view.bluetooth_tab import BluetoothTab
from components.view.radio_tab import RadioTab
from components.view.settings_tab import SettingsTab
from components.view.soundboard_tab import SoundboardTab
from components.view.taskbar import Taskbar
from core.factories.helper_factories import (
    create_player_helper,
    create_theme_helper,
)
from core.factories.settings_factories import create_party_mode_settings
from helper.bluetooth_helper import BluetoothHelper
from helper.constants import Constants
from helper.page_state import PageState

bluetooth_helper = BluetoothHelper()


class Tabs:
    taskbar: Taskbar = None
    radio_tab: RadioTab = None
    bluetooth_tab: BluetoothTab = None
    settings_tab: SettingsTab = None

    def __init__(
        self,
        taskbar: Taskbar,
        radio_tab: RadioTab,
        bluetooth_tab: BluetoothTab,
        soundboard_tab: SoundboardTab,
        settings_tab: SettingsTab,
    ):
        self.theme_helper = create_theme_helper()
        self.party_mode_settings = create_party_mode_settings()

        self.taskbar = taskbar
        self.radio_tab = radio_tab
        self.bluetooth_tab = bluetooth_tab
        self.soundboard_tab = soundboard_tab
        self.settings_tab = settings_tab

        self.player = create_player_helper()

    def change_tab(self, e):
        PageState.page.theme_mode = self.theme_helper.get_theme()
        PageState.page.update()

        new_tab_index = e.control.selected_index
        self.radio_tab.get_song_info().reset()

        try:
            self.radio_tab.hide()
            self.bluetooth_tab.hide()
            self.settings_tab.hide()
            self.soundboard_tab.hide()
        except Exception:
            pass

        if new_tab_index == 0:
            self.switch_radio_tab()

        if new_tab_index == 1:
            self.switch_bluetooth_tab()

        if new_tab_index == 2:
            if self.party_mode_settings.is_party_mode():
                self.switch_soundboard_tab()
            else:
                self.switch_settings_tab()

        if new_tab_index == 3:
            self.settings_tab.show()

    def switch_radio_tab(self):
        if bluetooth_helper.is_discovery_on():
            self.bluetooth_tab.get_btn_toggle().toggle_bluetooth_discovery()

        bluetooth_helper.disconnect()
        time.sleep(0.2)
        bluetooth_helper.turn_off()

        self.radio_tab.show()
        self.radio_tab.update()
        self.taskbar.update()

    def switch_bluetooth_tab(self):
        Constants.current_radio_station = {}

        self.player.pause()
        bluetooth_helper.turn_on()

        self.taskbar.update()

        self.bluetooth_tab.show()

        self.radio_tab.get_grid().disable_indicator()
        self.radio_tab.get_song_info().reset()

    def switch_soundboard_tab(self):
        self.soundboard_tab.show()

    def switch_settings_tab(self):
        self.settings_tab.show()
