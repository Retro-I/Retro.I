from enum import StrEnum

import flet as ft
from flet_contrib.color_picker.src.color_picker import ColorPicker

from helper.ColorHelper import ColorHelper
from helper.SplashscreenHelper import SplashscreenHelper
from helper.StripSettingsHelper import StripSettingsHelper

splashscreen_helper = SplashscreenHelper()
settings_helper = StripSettingsHelper()
color_helper = ColorHelper()


class LedTypeEnum(StrEnum):
    AUTOMATIC = "automatic"
    STATIC = "static"


class LedColorDialog(ft.AlertDialog):
    def __init__(self, strip, parent_dialog):
        super().__init__(on_dismiss=self._on_dismiss)

        self.strip = strip

        self.color_picker = MyColorPicker(
            strip=self.strip, color=settings_helper.get_static_color()
        )
        self.color_picker.visible = settings_helper.is_static_color()

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
        settings_helper.update_settings(static_color=self.color_picker.color)

    def open_dialog(self):
        self.open = True
        self.color_picker.visible = settings_helper.is_static_color()
        self.color_picker.color = settings_helper.get_static_color()
        self.update()


class MyColorPicker(ColorPicker):
    def __init__(self, strip, color):
        super().__init__()
        self.strip = strip
        self.color = color

    @ColorPicker.color.setter
    def color(self, value):
        ColorPicker.color.fset(self, value)
        if settings_helper.is_static_color():
            self.strip.set_color(color_helper.toRgb(value))
