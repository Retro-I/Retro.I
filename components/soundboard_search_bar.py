import flet as ft

from components.dialogs.soundboard_search_dialog import SoundboardSearchDialog
from helper.constants import Constants
from helper.page_state import PageState

constants = Constants()


class SoundboardSearchBar(ft.Container):
    soundboard_search_dialog: SoundboardSearchDialog = None

    def __init__(self, on_favorite_add):
        super().__init__()

        self.soundboard_search_dialog = SoundboardSearchDialog(on_favorite_add)
        self.content = ft.Row(
            [
                ft.Text("", expand=True),
                ft.TextButton(
                    "Soundboard durchsuchen",
                    icon=ft.Icons.SEARCH,
                    on_click=lambda e: PageState.page.show_dialog(
                        self.soundboard_search_dialog
                    ),  # noqa:E501
                    # style=ft.ButtonStyle(
                    #    text_style=ft.TextStyle(size=16)
                    # )
                ),
            ]
        )
        self.border = ft.border.only(bottom=ft.border.BorderSide(1, "gray"))
        self.padding = ft.padding.only(bottom=10)
