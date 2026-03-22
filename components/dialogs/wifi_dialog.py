import asyncio

import flet as ft

from components.dialogs.wifi_connection_dialog import WifiConnectionDialog
from components.scrollbar import with_scrollbar_space
from core.factories.helper_factories import (
    create_system_helper,
    create_wifi_helper,
)


class WifiDialog(ft.AlertDialog):
    loading = ft.ProgressRing(visible=False)
    not_found = ft.Text("Keine Netzwerke gefunden", visible=False)
    listview = with_scrollbar_space(
        ft.ListView(spacing=10, padding=20, expand=True, visible=False)
    )

    connection_dialog: WifiConnectionDialog = None

    def __init__(self, connection_dialog: WifiConnectionDialog, on_toggle_wifi):
        super().__init__()

        self.system_helper = create_system_helper()
        self.wifi_helper = create_wifi_helper()

        self.connection_dialog = connection_dialog
        self.on_toggle_wifi = on_toggle_wifi

        self.toggle_wifi_switch = ft.Switch(
            label="Wifi einschalten",
            label_text_style=ft.TextStyle(size=18),
            on_change=lambda e: self.toggle_wifi(),
            value=self.wifi_helper.is_enabled(),
        )

        self.content = ft.Column(
            [
                self.toggle_wifi_switch,
                ft.Divider(),
                ft.Text(
                    "Verfügbare Netzwerke:", size=20, weight=ft.FontWeight.BOLD
                ),
                ft.Column(
                    width=500,
                    expand=True,
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        self.loading,
                        self.not_found,
                        self.listview,
                    ],
                ),
            ]
        )

    async def open_dialog(self):
        self.open = True
        self.toggle_wifi_switch.value = wifi_helper.is_enabled()
        self.toggle_wifi_switch.update()

        self.listview.visible = False
        self.not_found.visible = False
        self.update()

        if not self.wifi_helper.is_enabled():
            return

        self.loading.visible = True
        self.listview.controls = []
        self.update()

        curr_ssid = self.system_helper.get_current_ssid()
        networks = await asyncio.to_thread(self.wifi_helper.get_networks)

        for n in networks:
            ico = ft.Icon(ft.Icons.DONE, size=28, visible=False)
            btn = ft.TextButton(
                content=ft.Container(
                    content=ft.Row(controls=[ico, ft.Text(n, size=16)])
                ),
                on_click=lambda e, name=n: self.connection_dialog.open_dialog(
                    name
                ),
            )

            if curr_ssid == n:
                ico.visible = True

            self.listview.controls.append(btn)

        self.loading.visible = False

        if len(networks) == 0:
            self.not_found.visible = True

        self.listview.visible = True
        self.update()

    def toggle_wifi(self):
        self.wifi_helper.toggle_wifi()
        self.on_toggle_wifi()

        self.listview.visible = not self.wifi_helper.is_enabled()
        self.page.run_task(self.open_dialog)

    def close(self):
        self.open = False
        self.update()
