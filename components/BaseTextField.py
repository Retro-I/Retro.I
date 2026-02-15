import flet as ft

from core.helpers.factories.system import create_system_helper


class BaseTextField(ft.TextField):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.system_helper = create_system_helper()

        self.on_focus = lambda e: self.system_helper.open_keyboard()
        self.on_blur = lambda e: self.system_helper.close_keyboard()
