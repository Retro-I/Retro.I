import asyncio

import flet as ft

from components.base_text_field import BaseTextField
from components.scrollbar import with_scrollbar_space
from core.factories.helper_factories import (
    create_audio_helper,
    create_sounds_helper,
)
from helper.constants import Constants

constants = Constants()


class SoundboardSearchDialog(ft.AlertDialog):
    text = ft.Text("")

    loading = ft.ProgressRing(visible=False)
    not_found_text = ft.Text("Keine Sounds gefunden!", visible=False)
    listview = with_scrollbar_space(
        ft.ListView(spacing=10, expand=True, visible=False)
    )
    search_textfield = BaseTextField(label="Sounds", expand=True)

    on_favorite_add = None

    def __init__(self, on_favorite_add):
        super().__init__()

        self.on_favorite_add = on_favorite_add

        self.audio_state = create_audio_helper()
        self.sounds_helper = create_sounds_helper()

        self.content = ft.Column(
            width=600,
            expand=True,
            tight=True,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Row(
                    [
                        self.search_textfield,
                        ft.FilledButton("Suchen", on_click=self.search_sounds),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                ft.Column(
                    controls=[self.loading, self.not_found_text, self.listview],
                    expand=True,
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
            ],
        )

    def open_dialog(self):
        self.open = True
        self.update()

    def close(self):
        self.open = False
        self.update()

    async def search_sounds(self, _):
        self.listview.visible = False
        self.not_found_text.visible = False
        self.loading.visible = True
        self.update()

        query = self.search_textfield.value

        sounds = await asyncio.to_thread(
            self.sounds_helper.search_sounds, query
        )

        self.loading.visible = False
        self.not_found_text.visible = len(sounds) == 0

        self.listview.controls.clear()

        for el in sounds:
            fav_btn = ft.IconButton(
                icon=ft.Icons.PLAYLIST_ADD,
                on_click=lambda e, item=el: self.on_favorite_add(item),
            )

            img = ft.Image(
                constants.get_button_img(),
                fit=ft.BoxFit.SCALE_DOWN,
                border_radius=ft.border_radius.all(10),
                width=66,
                height=66,
            )
            element = ft.Row(
                [
                    ft.Container(
                        content=ft.Row(
                            [
                                img,
                                ft.Text(
                                    el["title"],
                                    weight=ft.FontWeight.BOLD,
                                    size=20,
                                    expand=True,
                                ),
                            ]
                        ),
                        on_click=lambda e, item=el: self.play_sound(item),
                        expand=True,
                    ),
                    fav_btn,
                ]
            )

            self.listview.controls.append(element)

        self.listview.visible = True
        self.update()

    def play_sound(self, item):
        self.audio_state.play_sound_board(item["mp3"])
