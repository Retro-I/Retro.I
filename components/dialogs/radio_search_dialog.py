import flet as ft

from components.base_text_field import BaseTextField
from components.dialogs.station_add_dialog import StationAddDialog
from components.radio_grid import RadioGrid
from components.scrollbar import with_scrollbar_space
from core.factories.helper_factories import create_radio_meta_helper
from helper.constants import Constants

constants = Constants()


class RadioSearchDialog(ft.AlertDialog):
    text = ft.Text("")

    loading = ft.ProgressRing(visible=False)
    not_found_text = ft.Text("Kein Radiosender gefunden!", visible=False)
    listview = with_scrollbar_space(
        ft.ListView(spacing=10, expand=True, visible=False)
    )
    search_textfield = BaseTextField(label="Radiosender", expand=True)

    station_add_dialog: StationAddDialog = None

    def __init__(self, radio_grid: RadioGrid):
        super().__init__()

        self.radio_meta_helper = create_radio_meta_helper()

        self.station_add_dialog = StationAddDialog(radio_grid)

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
                        ft.FilledButton(
                            "Suchen", on_click=lambda e: self.search_stations()
                        ),
                    ],
                    spacing=ft.MainAxisAlignment.SPACE_BETWEEN,
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

    def search_stations(self):
        self.listview.visible = False
        self.listview.update()

        self.not_found_text.visible = False
        self.not_found_text.update()

        self.loading.visible = True
        self.loading.update()

        name = self.search_textfield.value
        stations = self.radio_meta_helper.get_stations_by_name(name)

        self.loading.visible = False
        self.loading.update()

        if len(stations) == 0:
            self.not_found_text.visible = True
        else:
            self.not_found_text.visible = False

        self.not_found_text.update()

        self.listview.controls = []
        for el in stations:
            img = ft.Container(
                ft.Icon(ft.Icons.MUSIC_NOTE), width=60, height=60
            )
            if el["logo"] != "":
                img = ft.Image(
                    el["logo"],
                    fit=ft.BoxFit.SCALE_DOWN,
                    border_radius=ft.border_radius.all(10),
                    width=50,
                    height=50,
                )

            element = ft.Container(
                content=ft.Row(
                    controls=[
                        img,
                        ft.Column(
                            expand=True,
                            controls=[
                                ft.Text(el["name"], weight=ft.FontWeight.BOLD),
                                ft.Text(el["src"]),
                            ],
                        ),
                    ]
                ),
                on_click=lambda e, item=el: self.station_add_dialog.open_dialog(
                    item
                ),
            )

            self.listview.controls.append(element)

        self.listview.visible = True
        self.listview.update()
