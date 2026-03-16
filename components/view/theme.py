import flet as ft

from components.navigation_bar import NavigationBar
from components.view.bluetooth_tab import BluetoothTab
from components.view.radio_tab import RadioTab
from components.view.settings_tab import SettingsTab
from components.view.soundboard_tab import SoundboardTab
from components.view.tabs import Tabs
from components.view.taskbar import Taskbar
from core.factories.settings_factories import (
    create_party_mode_settings,
    create_scrollbar_settings,
)
from helper.page_state import PageState


class Theme:
    def __init__(self, taskbar: Taskbar, strip):
        self.scrollbar_settings_helper = create_scrollbar_settings()
        self.party_mode_settings = create_party_mode_settings()

        self.taskbar = taskbar

        self.theme = ft.Theme(
            color_scheme_seed="green",
            scrollbar_theme=self.get_scrollbar_theme(),
        )

        self.radio_tab = RadioTab(
            self.on_updated_radio_station,
            self.on_stop_radio_station,
        )
        self.bluetooth_tab = BluetoothTab()
        self.soundboard_tab = SoundboardTab()
        self.settings_tab = SettingsTab(strip)
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

    def on_stop_radio_station(self):
        self.radio_tab.song_info_row.reset()
        self.update()

    def on_updated_radio_station(self, color):
        self.theme = ft.Theme(
            color_scheme_seed=color,
            scrollbar_theme=self.get_scrollbar_theme(),
        )

        PageState.page.theme = self.theme
        PageState.page.dark_theme = self.theme
        self.navbar.update_color(color)
        self.radio_tab.update()

        PageState.page.update()

    def get_tabs(self):
        tabs = []
        tabs.append(self.radio_tab)
        tabs.append(self.bluetooth_tab)

        if self.party_mode_settings.is_party_mode():
            tabs.append(self.soundboard_tab)

        tabs.append(self.settings_tab)

        return tabs

    def get_scrollbar_theme(self) -> ft.ScrollbarTheme:
        scrollbar_theme = ft.ScrollbarTheme(
            thumb_visibility=False, track_visibility=False
        )

        if self.scrollbar_settings_helper.is_scrollbar_enabled():
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
