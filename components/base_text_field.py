import flet as ft

from helper.SystemHelper import SystemHelper

system_helper = SystemHelper()


class BaseTextField(ft.TextField):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.on_focus = lambda e: system_helper.open_keyboard()
        self.on_blur = lambda e: system_helper.close_keyboard()
