import flet as ft

from components.view.Tabs import Tabs
from core.enums.tabs_enum import TabsEnum
from core.helpers.factories.system import create_system_helper

ICON_SIZE = 28


class NavigationBar(ft.NavigationBar):
    def __init__(self, tabs: Tabs, target_tabs):
        super().__init__()

        self.system_helper = create_system_helper()

        self.bgcolor = "green"
        self.on_change = tabs.change_tab
        self.selected_index = 0
        self.destinations = self.get_destinations(target_tabs)

    def update_color(self, color):
        self.bgcolor = color
        self.update()
        for i in self.destinations:
            i.update()

    def get_destinations(self, target_tabs):
        destinations = []
        if TabsEnum.RADIO in target_tabs:
            destinations.append(
                ft.NavigationBarDestination(
                    label="Radiosender",
                    icon=ft.Icon(
                        ft.Icons.RADIO_OUTLINED,
                        size=ICON_SIZE,
                        color=ft.Colors.ON_SURFACE,
                    ),
                    selected_icon=ft.Icon(ft.Icons.RADIO, size=ICON_SIZE),
                )
            )

        if TabsEnum.BLUETOOTH in target_tabs:
            destinations.append(
                ft.NavigationBarDestination(
                    label="Bluetooth",
                    icon=ft.Icon(
                        ft.Icons.BLUETOOTH_OUTLINED,
                        size=ICON_SIZE,
                        color=ft.Colors.ON_SURFACE,
                    ),
                    selected_icon=ft.Icon(ft.Icons.BLUETOOTH, size=ICON_SIZE),
                )
            )

        if (
            TabsEnum.SOUNDBOARD in target_tabs
            and self.system_helper.is_party_mode()
        ):
            destinations.append(
                ft.NavigationBarDestination(
                    label="Soundboard",
                    icon=ft.Icon(
                        ft.Icons.SPACE_DASHBOARD_OUTLINED,
                        size=ICON_SIZE,
                        color=ft.Colors.ON_SURFACE,
                    ),
                    selected_icon=ft.Icon(
                        ft.Icons.SPACE_DASHBOARD, size=ICON_SIZE
                    ),
                ),
            )

        if TabsEnum.SETTINGS in target_tabs:
            destinations.append(
                ft.NavigationBarDestination(
                    label="Einstellungen",
                    icon=ft.Icon(
                        ft.Icons.SETTINGS_OUTLINED,
                        size=ICON_SIZE,
                        color=ft.Colors.ON_SURFACE,
                    ),
                    selected_icon=ft.Icon(ft.Icons.SETTINGS, size=ICON_SIZE),
                )
            )

        return destinations
