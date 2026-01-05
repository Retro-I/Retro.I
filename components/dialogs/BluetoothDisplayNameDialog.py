import flet as ft

from components.BaseTextField import BaseTextField
from helper.BluetoothHelper import BluetoothHelper

bluetooth_helper = BluetoothHelper()


class BluetoothDisplayNameDialog(ft.AlertDialog):
    def __init__(self, on_submit):
        super().__init__()

        self.on_submit = on_submit

        self.display_name_textfield = BaseTextField(
            value=bluetooth_helper.get_bluetooth_display_name(),
            label="Anzeigename",
        )

        self.title = ft.Text("Bluetooth Anzeigename")
        self.content = ft.Column(
            alignment=ft.MainAxisAlignment.CENTER,
            width=500,
            tight=True,
            controls=[self.display_name_textfield],
        )
        self.actions = [
            ft.TextButton("Abbrechen", on_click=lambda e: self.close()),
            ft.FilledButton("Speichern", on_click=lambda e: self.on_save()),
        ]

    def on_save(self):
        bluetooth_helper.change_bluetooth_display_name(self.display_name_textfield.value)
        self.on_submit()
        self.close()

    def open_dialog(self):
        self.open = True
        self.update()

    def close(self):
        self.open = False
        self.update()
