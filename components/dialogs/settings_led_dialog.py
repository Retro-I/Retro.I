import flet as ft

from components.dialogs.led_color_dialog import LedColorDialog, LedTypeEnum
from core.factories.helper_factories import create_color_helper
from core.factories.settings_factories import create_strip_settings
from helper.page_state import PageState


class SettingsLedDialog(ft.AlertDialog):
    def __init__(self, strip):
        super().__init__()

        self.settings_helper = create_strip_settings()
        self.color_helper = create_color_helper()

        self.strip = strip

        self.led_color_dialog = LedColorDialog(strip, self)
        PageState.page.add(self.led_color_dialog)

        self.radio_group = ft.RadioGroup(
            on_change=self.handle_selection_change,
            value=(
                LedTypeEnum.STATIC
                if self.settings_helper.is_static_color()
                else LedTypeEnum.AUTOMATIC
            ),
            content=ft.Column(
                controls=[
                    ft.Radio(value=LedTypeEnum.AUTOMATIC, label="Automatisch"),
                    ft.Radio(value=LedTypeEnum.STATIC, label="Statische Farbe"),
                ]
            ),
        )
        self.btn_open_led_dialog = ft.TextButton(
            "Farbe ändern",
            style=ft.ButtonStyle(text_style=ft.TextStyle(size=20)),
            on_click=lambda e: self.open_led_color_dialog(),
            icon=ft.Icons.OPEN_IN_NEW,
        )

        self.title = ft.Text("LED-Streifen")
        self.content = ft.Column(
            alignment=ft.MainAxisAlignment.CENTER,
            width=500,
            expand=True,
            controls=[
                ft.Switch(
                    "LED-Streifen einschalten",
                    label_style=ft.TextStyle(size=18),
                    on_change=strip.toggle_strip,
                    value=self.settings_helper.is_strip_active(),
                ),
                ft.Divider(),
                ft.Column(
                    [
                        ft.Text("Helligkeit:", style=ft.TextStyle(size=20)),
                        ft.Slider(
                            on_change=lambda e: strip.change_brightness(
                                e.control.value
                            ),
                            min=0,
                            max=100,
                            value=self.settings_helper.get_curr_brightness(),
                            expand=True,
                        ),
                    ]
                ),
                ft.Divider(),
                self.radio_group,
                self.btn_open_led_dialog,
            ],
        )

    def handle_selection_change(self, e):
        if e.control.value == LedTypeEnum.AUTOMATIC:
            self.settings_helper.update_settings(is_static_color=False)
            self.btn_open_led_dialog.visible = False
            self.strip.set_color(self.strip.curr_station_color)
        elif e.control.value == LedTypeEnum.STATIC:
            self.settings_helper.update_settings(is_static_color=True)
            self.btn_open_led_dialog.visible = True
            color = self.color_helper.to_rgb(
                self.led_color_dialog.color_picker.color
            )
            self.strip.set_color(color)
        self.btn_open_led_dialog.update()

    def open_led_color_dialog(self):
        self.led_color_dialog.open_dialog()

    def open_dialog(self):
        self.btn_open_led_dialog.visible = (
            self.settings_helper.is_static_color()
        )
        self.btn_open_led_dialog.update()
        self.open = True
        self.update()
