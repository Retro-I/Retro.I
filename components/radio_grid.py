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
            placeholder_src="data:image/png;base64,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",  # noqa: E501
            placeholder_fit=ft.BoxFit.FIT_WIDTH,
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
