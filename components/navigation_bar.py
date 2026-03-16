import flet as ft

from components.view.tabs import Tabs
from core.factories.settings_factories import create_party_mode_settings


class NavigationBar(ft.NavigationBar):
    def __init__(self, tabs: Tabs):
        super().__init__()

        self.party_mode_settings = create_party_mode_settings()

        self.bgcolor = ft.Colors.GREEN
        self.on_change = tabs.change_tab
        self.selected_index = 0
        self.destinations = self.get_destinations()

    def update_color(self, color):
        self.bgcolor = color
        self.update()
        for i in self.destinations:
            i.update()

    def get_destinations(self):
        destinations = [
            ft.NavigationBarDestination(
                label="Radiosender",
                icon=ft.Icons.RADIO_OUTLINED,
                selected_icon=ft.Icons.RADIO,
            ),
            ft.NavigationBarDestination(
                label="Bluetooth",
                icon=ft.Icons.BLUETOOTH_OUTLINED,
                selected_icon=ft.Icons.BLUETOOTH,
            ),
        ]

        if self.party_mode_settings.is_party_mode():
            destinations.append(
                ft.NavigationBarDestination(
                    label="Soundboard",
                    icon=ft.Icons.SPACE_DASHBOARD_OUTLINED,
                    selected_icon=ft.Icons.SPACE_DASHBOARD,
                ),
            )

        destinations.append(
            ft.NavigationBarDestination(
                label="Einstellungen",
                icon=ft.Icons.SETTINGS_OUTLINED,
                selected_icon=ft.Icons.SETTINGS,
            )
        )

        return destinations
