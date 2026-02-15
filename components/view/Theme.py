import flet as ft

from core.app_platform import get_app_platform, AppPlatform
from core.enums.tabs_enum import TabsEnum
from core.helpers.factories.system import create_system_helper
from core.settings.factories.scrollbar import create_scrollbar_settings

if get_app_platform() == AppPlatform.PI:
    from scripts import button
from components.NavigationBar import NavigationBar
from components.view.Tabs import Tabs
from components.view.tabs.BluetoothTab import BluetoothTab
from components.view.tabs.RadioTab import RadioTab
from components.view.tabs.SettingsTab import SettingsTab
from components.view.tabs.SoundboardTab import SoundboardTab
from helper.PageState import PageState


class Theme:
    def __init__(self, target_tabs=[]):
        if target_tabs is None:
            target_tabs = [
                TabsEnum.RADIO,
                TabsEnum.BLUETOOTH,
                TabsEnum.SOUNDBOARD,
                TabsEnum.SETTINGS,
            ]
        self.scrollbar_settings = create_scrollbar_settings()
        self.system_helper = create_system_helper()

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
        self.settings_tab = SettingsTab()
        self.tabs = Tabs(
            self.radio_tab,
            self.bluetooth_tab,
            self.soundboard_tab,
            self.settings_tab,
        )
        self.navbar = NavigationBar(self.tabs, target_tabs)

    def update(self):
        PageState.page.update()

    def on_stop_radio_station(self):
        self.radio_tab.song_info_row.reset()
        self.update()

    def on_updated_radio_station(self, color):
        self.theme.color_scheme_seed = color
        self.navbar.update_color(color)
        self.radio_tab.update()
        PageState.page.update()

    def get_tabs(self):
        tabs = []
        tabs.append(self.radio_tab)
        tabs.append(self.bluetooth_tab)

        if self.system_helper.is_party_mode():
            tabs.append(self.soundboard_tab)

        tabs.append(self.settings_tab)

        return tabs

    def get_scrollbar_theme(self) -> ft.ScrollbarTheme:
        scrollbar_theme = ft.ScrollbarTheme(
            thumb_visibility=False, track_visibility=False
        )

        if self.scrollbar_settings.is_scrollbar_enabled():
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
