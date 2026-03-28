import flet as ft

from core.helpers.factories.audio import create_audio_helper
from helper.Constants import Constants

c = Constants()


class SoundCard(ft.Column):
    def __init__(self, sound, on_delete_favorite_sound):
        super().__init__()

        self.audio_state = create_audio_helper()

        self.controls = [
            ft.Container(
                alignment=ft.alignment.bottom_center,
                on_click=lambda e, src=sound[
                    "mp3"
                ]: self.audio_state.play_sound_board(src),
                on_long_press=lambda e, src=sound: on_delete_favorite_sound(
                    src
                ),
                content=ft.Image(
                    src=c.get_button_img(),
                    border_radius=ft.border_radius.all(4),
                    fit=ft.ImageFit.FIT_WIDTH,
                ),
                height=130,
            ),
            ft.Container(
                ft.Text(
                    sound["title"], size=20, text_align=ft.TextAlign.CENTER
                ),
                width=300,
            ),
        ]
