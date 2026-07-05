from datetime import time

import flet as ft

from core.factories.settings_factories import (
    create_power_management_settings,
)


class SettingsPowerManagerDialog(ft.AlertDialog):
    def __init__(self):
        super().__init__()
        self.rows = []
        self.power_management_settings = create_power_management_settings()
        self.settings = self.power_management_settings.get_management_settings()
        self.selected_item = None
        self.update_rows()

        self.rows_column = ft.Column(controls=self.rows)

        self.switch = ft.Switch(
            "Shutdown-Management",
            label_style=ft.TextStyle(size=18),
            on_change=self.on_toggle,
            value=self.power_management_settings.is_enabled(),
        )

        self.time_picker = ft.TimePicker(
            value=time(hour=19, minute=30),
            confirm_text="Speichern",
            cancel_text="Abbrechen",
            help_text="Zeit auswählen",
            error_invalid_text="Falsche Eingabe",
            time_picker_entry_mode=ft.TimePickerEntryMode.DIAL,
            on_change=self.handle_change,
        )

        self.content = ft.Column(
            width=500,
            tight=True,
            controls=[
                self.time_picker,
                self.switch,
                ft.Divider(),
                self.rows_column,
            ],
        )

    def on_toggle(self, event):
        if event.control.value:
            self.power_management_settings.enable_power_management()
        else:
            self.power_management_settings.disable_power_management()

        # TODO - make sure some thread is running that looks for shutdown time

    def open_dialog(self):
        self.open = True
        self.switch.value = self.power_management_settings.is_enabled()
        self.settings = self.power_management_settings.get_management_settings()
        self.update_rows()
        self.update()

    def update_rows(self):
        self.rows = [
            ft.Row(
                controls=[
                    ft.Checkbox(
                        value=item["enabled"],
                        label=item["name"],
                        on_change=lambda e, i=item: self.on_toggle_day(e, i),
                    ),
                    ft.TextButton(
                        text=item["time"],
                        on_click=lambda e, i=item: self.open_time_picker(i),
                        style=ft.ButtonStyle(text_style=ft.TextStyle(size=16)),
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            )
            for item in self.power_management_settings.get_management_settings()
        ]

        if hasattr(self, "rows_column"):
            self.rows_column.controls = self.rows
            self.rows_column.update()

    def open_time_picker(self, item: dict):
        hour = int(item["time"].split(":")[0])
        minute = int(item["time"].split(":")[1])
        self.selected_item = item
        self.time_picker.value = time(hour=hour, minute=minute)
        self.time_picker.open = True
        self.time_picker.update()

    def on_toggle_day(self, event, item):
        item["enabled"] = event.control.value
        self.power_management_settings.update_management_settings(item)

    def handle_change(self, event):
        self.selected_item["time"] = self.time_picker.value.strftime("%H:%M")
        self.power_management_settings.update_management_settings(
            self.selected_item
        )
        self.update_rows()
