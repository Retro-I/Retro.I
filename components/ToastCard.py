import flet as ft

from helper.Audio import Audio
from helper.Constants import Constants

c = Constants()
audio_helper = Audio()


class ToastCard(ft.Column):
    def __init__(self):
        super().__init__()

        self.width = 300
        self.controls = [
            ft.Container(
                alignment=ft.alignment.bottom_center,
                on_click=lambda e: audio_helper.play_toast(),
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
