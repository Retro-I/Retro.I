import flet as ft

from helper.ScrollbarSettingsHelper import ScrollbarSettingsHelper
from helper.StartupErrorHelper import StartupErrorHelper
from scripts import button
from components.NavigationBar import NavigationBar
from components.view.Tabs import Tabs
from components.view.tabs.BluetoothTab import BluetoothTab
from components.view.tabs.RadioTab import RadioTab
from components.view.tabs.SettingsTab import SettingsTab
from components.view.tabs.SoundboardTab import SoundboardTab
from components.view.Taskbar import Taskbar
from helper.PageState import PageState
from helper.SystemHelper import SystemHelper

system_helper = SystemHelper()
scrollbar_settings_helper = ScrollbarSettingsHelper()


class Theme:
    theme = None
    taskbar: Taskbar = None

    radio_tab = None
    bluetooth_tab = None
    soundboard_tab = None
    settings_tab = None

    tabs = None
    navbar = None

    def __init__(self, taskbar: Taskbar, on_strip_run_color):
        self.taskbar = taskbar

        self.theme = ft.Theme(
            color_scheme_seed="green",
            scrollbar_theme=self.get_scrollbar_theme(),
        )

        self.radio_tab = RadioTab(on_strip_run_color, self.on_updated_radio_station, self.update)
        self.bluetooth_tab = BluetoothTab(self.taskbar)
        self.soundboard_tab = SoundboardTab()
        self.settings_tab = SettingsTab()
        self.tabs = Tabs(
            taskbar,
            self.radio_tab,
            self.bluetooth_tab,
            self.soundboard_tab,
            self.settings_tab,
        )
        self.navbar = NavigationBar(self.tabs)

    def update(self):
        PageState.page.update()

    def on_updated_radio_station(self, color):
        self.theme.color_scheme_seed = color
        self.navbar.update_color(color)
        self.radio_tab.update()
        PageState.page.update()

    def get_tabs(self):
        tabs = []
        tabs.append(self.radio_tab)
        tabs.append(self.bluetooth_tab)

        if system_helper.is_party_mode():
            tabs.append(self.soundboard_tab)

        tabs.append(self.settings_tab)

        return tabs

    def get_scrollbar_theme(self) -> ft.ScrollbarTheme:
        scrollbar_theme = ft.ScrollbarTheme(thumb_visibility=False, track_visibility=False)

        if scrollbar_settings_helper.is_scrollbar_enabled():
            scrollbar_theme = ft.ScrollbarTheme(
                track_color={
                    ft.ControlState.DEFAULT: ft.Colors.TRANSPARENT,
                },
                thumb_visibility=True,
                thumb_color={
                    ft.ControlState.HOVERED: ft.Colors.GREY_500,
                    ft.ControlState.DEFAULT: ft.Colors.GREY_400,
                },
                thickness=40,
                radius=20,
            )

        return scrollbar_theme

    def get(self):
        return self.theme

    def get_radio_tab(self):
        return self.radio_tab
