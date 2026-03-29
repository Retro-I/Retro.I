import flet as ft

from core.factories.helper_factories import create_audio_helper
from helper.constants import Constants

c = Constants()


class ToastCard(ft.Column):
    def __init__(self):
        super().__init__()

        self.audio_state = create_audio_helper()

        self.width = 300
        self.controls = [
            ft.Container(
                alignment=ft.alignment.bottom_center,
                on_click=lambda e: self.audio_state.play_toast(),
                height=130,
                content=ft.Image(src=c.get_button_img(), opacity=0.7),
            ),
            ft.Container(
                ft.Text(
                    "Zufälliger Trinkspruch",
                    size=20,
                    text_align=ft.TextAlign.CENTER,
                ),
                width=300,
            ),
        ]
