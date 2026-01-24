import flet as ft

from components.BaseTextField import BaseTextField
from helper.SystemHelper import SystemHelper
from helper.WifiHelper import WifiHelper

system_helper = SystemHelper()
wifi_helper = WifiHelper()


class WifiConnectionDialog(ft.AlertDialog):
    ssid = ft.Text("", size=24, weight=ft.FontWeight.BOLD)
    password = BaseTextField(
        password=True, can_reveal_password=True, autofocus=True
    )

    def __init__(self, on_connect):
        super().__init__()

        self.btn_connect = ft.FilledButton(
            "Verbinden",
            style=ft.ButtonStyle(text_style=ft.TextStyle(size=16)),
            on_click=lambda e: self.connect(on_connect),
        )

        self.btn_cancel = ft.TextButton(
            "Abbrechen",
            style=ft.ButtonStyle(text_style=ft.TextStyle(size=16)),
            on_click=lambda e: self.close(),
        )

        self.actions = [self.btn_cancel, self.btn_connect]
        self.actions_alignment = ft.MainAxisAlignment.SPACE_BETWEEN
        self.content = ft.Column(
            width=400,
            tight=True,
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                self.ssid,
                ft.Row([ft.Text("Passwort:", size=18), self.password]),
            ],
        )

    def open_dialog(self, name):
        self.ssid.value = name
        self.ssid.update()
        self.open = True

        self.btn_connect.disabled = False
        self.btn_connect.text = "Verbinden"
        self.btn_connect.update()

        self.update()

    def close(self):
        self.open = False
        self.update()

    def connect(self, on_connect):
        self.btn_connect.disabled = True
        self.btn_connect.text = "Wird verbunden..."
        self.btn_connect.update()
        on_connect()

        wifi_helper.connect_to_wifi(self.ssid.value, self.password.value)

        self.password.value = ""

        self.close()
        self.btn_connect.disabled = False
        self.btn_connect.text = "Verbinden"
        on_connect()
