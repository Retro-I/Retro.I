import threading
import time

import flet as ft

from components.BluetoothDeviceConnected import BluetoothDeviceConnected
from components.BluetoothDiscoveryToggle import BluetoothDiscoveryToggle
from components.dialogs.BluetoothDisplayNameDialog import (
    BluetoothDisplayNameDialog,
)
from components.view.Taskbar import Taskbar
from helper.BluetoothHelper import BluetoothHelper
from helper.PageState import PageState

bluetooth_helper = BluetoothHelper()


class BluetoothTab(ft.Column):
    taskbar: Taskbar = None
    btn_toggle_discovery = None
    device_connected = None
    update_device_connection = False
    bluetooth_device_edit_dialog = None
    bluetooth_display_name = ft.TextSpan(
        "", style=ft.TextStyle(size=20, weight=ft.FontWeight.BOLD)
    )

    def __init__(self, taskbar: Taskbar):
        super().__init__()

        self.taskbar = taskbar
        self.btn_toggle_discovery = BluetoothDiscoveryToggle(
            self.start_bluetooth_update_process,
            self.stop_bluetooth_update_process,
        )
        self.device_connected = BluetoothDeviceConnected(
            taskbar, self.btn_toggle_discovery.disable_discovery, self.show
        )

        self.bluetooth_display_name_dialog = BluetoothDisplayNameDialog(
            self.show
        )
        PageState.page.add(self.bluetooth_display_name_dialog)

        self.alignment = ft.alignment.center
        self.expand = True
        self.visible = False
        self.controls = [
            ft.Row(
                spacing=50,
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                    self.btn_toggle_discovery,
                ],
            ),
            ft.Row(
                spacing=50,
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                    ft.Text(
                        spans=[
                            ft.TextSpan("Anzeigename: "),
                            self.bluetooth_display_name,
                        ]
                    ),
                    ft.FilledButton(
                        "Ändern",
                        on_click=lambda e: self.open_change_bluetooth_display_name_dialog(),  # noqa:E501
                    ),
                ],
            ),
            ft.Divider(),
            ft.Text(
                "Gekoppelte Geräte:",
                size=20,
                weight=ft.FontWeight.BOLD,
                text_align=ft.TextAlign.LEFT,
            ),
            self.device_connected.get(),
        ]

    def show(self):
        if not bluetooth_helper.is_connected():
            self.update_device_connection = True
            self.process_bluetooth_connection()

        self.bluetooth_display_name.text = (
            bluetooth_helper.get_bluetooth_display_name()
        )
        self.bluetooth_display_name.update()

        self.visible = True
        self.update()

    def hide(self):
        self.visible = False
        self.update_device_connection = False
        self.update()

    def open_change_bluetooth_display_name_dialog(self):
        self.bluetooth_display_name_dialog.open_dialog()

    def update_connected_device(self):
        while self.update_device_connection:
            connected = self.device_connected.update_connected_device()
            if connected:
                self.update_device_connection = False
            self.device_connected.reload_devices()
            time.sleep(1)

    def start_bluetooth_update_process(self):
        self.update_device_connection = True
        self.process_bluetooth_connection()

    def stop_bluetooth_update_process(self):
        self.update_device_connection = False

    def process_bluetooth_connection(self):
        process = threading.Thread(target=self.update_connected_device)
        process.start()

    def get_btn_toggle(self):
        return self.btn_toggle_discovery

    def get_device_connected(self):
        return self.device_connected
