import flet as ft

from components.BaseTextField import BaseTextField
from helper.AdminHelper import AdminHelper
from helper.SystemHelper import SystemHelper

system_helper = SystemHelper()
admin_password_helper = AdminHelper()


class AdminPasswordDialog(ft.AlertDialog):
    ssid = ft.Text("", size=24, weight=ft.FontWeight.BOLD)
    password = BaseTextField(
        password=True, can_reveal_password=True, autofocus=True
    )

    def __init__(self, on_connect):
        super().__init__()

        self.btn_ok = ft.FilledButton(
            "Ok",
            style=ft.ButtonStyle(text_style=ft.TextStyle(size=16)),
            on_click=lambda e: self.connect(on_connect),
        )

        self.btn_cancel = ft.TextButton(
            "Abbrechen",
            style=ft.ButtonStyle(text_style=ft.TextStyle(size=16)),
            on_click=lambda e: self.close(),
        )

        self.actions = [self.btn_cancel, self.btn_ok]
        self.actions_alignment = ft.MainAxisAlignment.SPACE_BETWEEN
        self.title = "Admin Passwort"
        self.content = ft.Column(
            width=400,
            tight=True,
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[self.password],
        )

    def open_dialog(self):
        self.password.value = ""
        self.password.error_text = ""
        self.password.update()
        self.open = True
        self.update()

    def close(self):
        self.open = False
        self.update()

    def connect(self, on_connect):
        if admin_password_helper.validate_admin_password(self.password.value):
            system_helper.toggle_party_mode()
            on_connect()
            return

        self.password.error_text = "Falsches Passwort!"
        self.password.update()
