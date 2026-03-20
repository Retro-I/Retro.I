import flet as ft

from components.dialogs.radio_search_dialog import RadioSearchDialog
from components.radio_grid import RadioGrid
from core.factories.helper_factories import create_radio_meta_helper
from helper.constants import Constants
from helper.page_state import PageState

constants = Constants()


class SongInfoRow(ft.Container):
    song_info_station = ft.Text(
        "Kein Radiosender ausgewählt", weight=ft.FontWeight.BOLD, size=16
    )
    song_info_title = ft.Text(
        "", size=16, overflow=ft.TextOverflow.ELLIPSIS, expand=True
    )

    radio_search_dialog: RadioSearchDialog = None

    def __init__(self, radio_grid: RadioGrid):
        super().__init__()

        self.radio_meta_helper = create_radio_meta_helper()

        self.radio_search_dialog = RadioSearchDialog(radio_grid)
        self.content = ft.Row(
            [
                ft.Icon(ft.Icons.MUSIC_NOTE, size=28),
                self.song_info_station,
                self.song_info_title,
                ft.TextButton(
                    "Sendersuche",
                    icon=ft.Icons.SEARCH,
                    on_click=lambda e: PageState.page.show_dialog(
                        self.radio_search_dialog
                    ),
                ),
            ]
        )
        self.border = ft.border.only(bottom=ft.border.BorderSide(1, "gray"))
        self.padding = ft.padding.only(bottom=10)

    def reload(self):
        try:
            title = self.radio_meta_helper.get_song_info(
                Constants.current_radio_station["src"]
            )

            if title != "":
                self.song_info_station.value = Constants.current_radio_station[
                    "name"
                ]
                self.song_info_title.value = title
            else:
                self.song_info_station.value = Constants.current_radio_station[
                    "name"
                ]
                self.song_info_title.value = ""
        except Exception:
            pass

        self.update()

    def update(self):
        self.song_info_station.update()
        self.song_info_title.update()
        super().update()

    def reset(self):
        self.song_info_station.value = "Kein Radiosender ausgewählt"
        self.song_info_title.value = ""
        self.update()
