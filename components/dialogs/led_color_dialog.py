from enum import StrEnum

import flet as ft
from flet_contrib.color_picker.src.color_picker import ColorPicker

from core.factories.helper_factories import create_color_helper
from core.factories.settings_factories import create_strip_settings


class LedTypeEnum(StrEnum):
    AUTOMATIC = "automatic"
    STATIC = "static"


class LedColorDialog(ft.AlertDialog):
    def __init__(self, strip, parent_dialog):
        super().__init__(on_dismiss=self._on_dismiss)
        self.settings_helper = create_strip_settings()

        self.strip = strip

        self.color_picker = MyColorPicker(
            strip=self.strip, color=self.settings_helper.get_static_color()
        )
        self.color_picker.visible = self.settings_helper.is_static_color()

        self.btn_back = ft.TextButton(
            "Zurück",
            on_click=lambda e: parent_dialog.open_dialog(),
            icon=ft.Icons.ARROW_BACK,
        )

        self.title = ft.Text("LED Farbe")
        self.content = ft.Column(
            width=600,
            height=500,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                self.color_picker,
            ],
        )
        self.actions = [self.btn_back]
        self.actions_alignment = ft.MainAxisAlignment.SPACE_BETWEEN

    def _on_dismiss(self, _):
        # Just save color on dialog close -> less times write to settings file
        self.settings_helper.update_settings(
            static_color=self.color_picker.color
        )

    def open_dialog(self):
        self.open = True
        self.color_picker.visible = self.settings_helper.is_static_color()
        self.color_picker.color = self.settings_helper.get_static_color()
        self.update()


class MyColorPicker(ColorPicker):
    def __init__(self, strip, color):
        super().__init__()
        self.color_helper = create_color_helper()
        self.settings_helper = create_strip_settings()

        self.strip = strip
        self.color = color

    @ColorPicker.color.setter
    def color(self, value):
        ColorPicker.color.fset(self, value)
        if self.settings_helper.is_static_color():
            self.strip.set_color(self.color_helper.to_rgb(value))
