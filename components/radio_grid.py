import flet as ft

from components.dialogs.station_modify_dialog import StationModifyDialog
from core.factories.helper_factories import (
    create_player_helper,
    create_strip_state,
    create_system_helper,
    create_theme_helper,
)
from core.factories.settings_factories import (
    create_radio_stations_settings,
)
from helper.constants import Constants
from helper.page_state import PageState

constants = Constants()


class RadioGrid(ft.GridView):
    def __init__(
        self,
        on_theme_change_radio_station,
        on_theme_stop_radio_station,
    ):
        super().__init__()

        self.strip_state = create_strip_state()
        self.player = create_player_helper()
        self.system_helper = create_system_helper()
        self.stations = create_radio_stations_settings()
        self.theme = create_theme_helper()

        self.station_modify_dialog = StationModifyDialog()
        self.on_theme_change_radio_station = on_theme_change_radio_station
        self.on_theme_stop_radio_station = on_theme_stop_radio_station

        PageState.page.add(self.station_modify_dialog)

        # Gridview attributes
        self.expand = True
        self.runs_count = 5
        self.max_extent = 150
        self.child_aspect_ratio = 1.0
        self.spacing = 20
        self.run_spacing = 50
        self.padding = ft.padding.only(top=12, left=8, right=8)

    def open_modify_station_dialog(self, station):
        self.station_modify_dialog.open_dialog(station, self.reload)

    def reload(self):
        self.controls.clear()
        Constants.indicator_refs = []
        favorite_station: object | None = self.stations.get_favorite_station()

        for i, station in enumerate(self.stations.load_radio_stations()):
            Constants.indicator_refs.append(ft.Ref[ft.Container]())
            self.controls.append(
                ft.Stack(
                    alignment=ft.Alignment.CENTER,
                    fit=ft.StackFit.EXPAND,
                    controls=[
                        ft.Container(
                            alignment=ft.Alignment.CENTER,
                            bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
                            on_click=lambda e, src=station, index=i: (
                                self.change_radio_station(src, index),
                            ),
                            on_long_press=lambda e, src=station, index=i: (
                                self.open_modify_station_dialog(src)
                            ),
                            border_radius=10,
                            content=self.get_content(station),
                            padding=10,
                        ),
                        ft.Container(
                            alignment=ft.Alignment.TOP_RIGHT,
                            on_click=lambda e, src=station, index=i: (
                                self.change_radio_station(src, index),
                            ),
                            on_long_press=lambda e, src=station, index=i: (
                                self.open_modify_station_dialog(src, index)
                            ),
                            visible=(
                                favorite_station is not None
                                and favorite_station["id"] == station["id"]
                            ),
                            padding=-10,
                            content=ft.Icon(
                                ft.Icons.FAVORITE,
                                color=ft.Colors.RED,
                                size=42,
                            ),
                        ),
                        ft.Container(
                            ref=Constants.indicator_refs[i],
                            alignment=ft.Alignment.TOP_LEFT,
                            on_click=lambda e: self.stop_radio_station(),
                            visible=(
                                Constants.current_radio_station != {}
                                and Constants.current_radio_station["id"]
                                == station["id"]
                            ),
                            padding=-10,
                            content=ft.Icon(
                                ft.Icons.PLAY_CIRCLE,
                                size=42,
                            ),
                        ),
                    ],
                )
            )
        self.update()

    def change_radio_station(self, station, index=-1):
        color = station["color"]
        Constants.current_radio_station = station

        self.toggle_indicator(index)

        self.player.play_src(station["src"])

        self.strip_state.update_strip(color)

        if self.on_theme_change_radio_station is not None:
            self.on_theme_change_radio_station(color)

    def stop_radio_station(self):
        Constants.current_radio_station = {}
        self.toggle_indicator()
        self.player.pause()
        self.on_theme_stop_radio_station()

    def disable_indicator(self):
        for ref in Constants.indicator_refs:
            ref.current.visible = False

    def toggle_indicator(self, index=-1):
        self.disable_indicator()
        if index != -1:
            Constants.indicator_refs[index].current.visible = True

    def get_logo(self, station):
        return ft.Image(
            src=self.system_helper.get_img_path(station["logo"]),
            border_radius=ft.border_radius.all(4),
            fit=ft.BoxFit.FIT_WIDTH,
        )

    def get_text(self, station):
        return ft.Text(
            station["name"],
            text_align=ft.TextAlign.CENTER,
            weight=ft.FontWeight.BOLD,
        )

    def get_content(self, station):
        if station["logo"] != "":
            return self.get_logo(station)

        return self.get_text(station)
