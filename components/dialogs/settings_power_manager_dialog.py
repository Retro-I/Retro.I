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

        self.update_rows()

        self.switch = ft.Switch(
            "Shutdown-Management aktiviert",
            label_style=ft.TextStyle(size=18),
            on_change=self.on_toggle,
            value=self.power_management_settings.is_enabled(),
        )

        self.content = ft.Column(
            width=500,
            tight=True,
            controls=[
                self.switch,
                ft.Divider(),
                *self.rows,
            ],
        )

    def on_toggle(self, control):
        if control.value:
            self.power_management_settings.enable_power_management()
        else:
            self.power_management_settings.disable_power_management()

        # TODO - make sure some thread is running that looks for shutdown time

    def on_toggle_day(self, control, item):
        item["enabled"] = control.value
        self.power_management_settings.update_management_settings(item)

    def open_dialog(self):
        self.open = True
        self.switch.value = self.power_management_settings.is_enabled()
        self.settings = self.power_management_settings.get_management_settings()
        self.update_rows()

        self.update()

    def update_rows(self):
        self.rows = [
            # TODO - maybe shorten this
            ft.Row(
                [
                    ft.Checkbox(
                        value=item["enabled"],
                        label=item["name"],
                        on_change=lambda e: self.on_toggle_day(e, item),
                    ),
                ]
            )
            for item in self.power_management_settings.get_management_items()
        ]
