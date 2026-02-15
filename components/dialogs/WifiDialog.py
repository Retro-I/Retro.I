import flet as ft

from components.dialogs.WifiConnectionDialog import WifiConnectionDialog
from components.Scrollbar import with_scrollbar_space
from core.helpers.factories.system import create_system_helper
from helper.WifiHelper import WifiHelper

wifi_helper = WifiHelper()


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

        self.connection_dialog = connection_dialog
        self.on_toggle_wifi = on_toggle_wifi

        self.toggle_wifi_switch = ft.Switch(
            "Wifi einschalten",
            label_style=ft.TextStyle(size=18),
            on_change=lambda e: self.toggle_wifi(),
            value=wifi_helper.is_enabled(),
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

    def open_dialog(self):
        self.open = True
        self.update()

        self.toggle_wifi_switch.value = wifi_helper.is_enabled()
        self.toggle_wifi_switch.update()

        self.listview.visible = False
        self.listview.update()

        self.not_found.visible = False
        self.not_found.update()

        if not wifi_helper.is_enabled():
            return

        self.loading.visible = True
        self.loading.update()

        self.listview.controls = []
        self.listview.update()

        curr_ssid = self.system_helper.get_current_ssid()
        networks = wifi_helper.get_networks()

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
        self.loading.update()

        if len(networks) == 0:
            self.not_found.visible = True
            self.not_found.update()

        self.listview.visible = True
        self.listview.update()

    def toggle_wifi(self):
        wifi_helper.toggle_wifi()
        self.on_toggle_wifi()

        if wifi_helper.is_enabled():
            self.listview.visible = False
            self.open_dialog()
        else:
            self.listview.visible = True
            self.open_dialog()

        self.listview.update()

    def close(self):
        self.open = False
        self.update()
