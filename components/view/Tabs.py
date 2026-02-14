import time

from components.view.tabs.BluetoothTab import BluetoothTab
from components.view.tabs.RadioTab import RadioTab
from components.view.tabs.SettingsTab import SettingsTab
from components.view.tabs.SoundboardTab import SoundboardTab
from core.app_state import AppState
from core.factories.audio_factory import create_audio_state
from helper.BluetoothHelper import BluetoothHelper
from helper.Constants import Constants
from helper.PageState import PageState
from helper.SystemHelper import SystemHelper
from helper.ThemeHelper import ThemeHelper

bluetooth_helper = BluetoothHelper()
system_helper = SystemHelper()
theme_helper = ThemeHelper()


class Tabs:
    radio_tab: RadioTab = None
    bluetooth_tab: BluetoothTab = None
    settings_tab: SettingsTab = None

    def __init__(
        self,
        radio_tab: RadioTab,
        bluetooth_tab: BluetoothTab,
        soundboard_tab: SoundboardTab,
        settings_tab: SettingsTab,
    ):
        self.audio_state = create_audio_state()

        self.radio_tab = radio_tab
        self.bluetooth_tab = bluetooth_tab
        self.soundboard_tab = soundboard_tab
        self.settings_tab = settings_tab

    def change_tab(self, e):
        PageState.page.theme_mode = theme_helper.get_theme()
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
            if system_helper.is_party_mode():
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
        AppState.app_state.update_taskbar()

    def switch_bluetooth_tab(self):
        Constants.current_radio_station = {}

        self.audio_state.pause()
        bluetooth_helper.turn_on()

        AppState.app_state.update_taskbar()

        self.bluetooth_tab.show()

        self.radio_tab.get_grid().disable_indicator()
        self.radio_tab.get_song_info().reset()

    def switch_soundboard_tab(self):
        self.soundboard_tab.show()

    def switch_settings_tab(self):
        self.settings_tab.show()
