import threading
import time

import flet as ft
from flet.core.types import AppView

from components.view.Theme import Theme
from core.app_state import AppState
from core.enums.tabs_enum import TabsEnum
from core.helpers.factories.theme import create_theme_helper
from helper.PageState import PageState

theme_helper = create_theme_helper()


def main(page: ft.Page):
    AppState()

    page.theme_mode = theme_helper.get_theme()
    page.update()

    PageState.page = page

    audio = ft.Audio(src="https://dispatcher.rndfnk.com/br/br1/nbopf/mp3/mid", autoplay=False)
    PageState.page.overlay.append(audio)
    PageState.audio = audio

    theme = Theme([TabsEnum.RADIO])

    page.navigation_bar = theme.navbar
    page.window.maximized = True
    page.window.frameless = True
    page.spacing = 0
    page.theme = theme.get()
    page.dark_theme = theme.get()
    page.title = "Retro.I"

    page.add(theme.radio_tab)

    theme.radio_tab.radio_grid.reload()

    page.update()

    page.on_error = None

    def background_processes():
        while True:
            theme.radio_tab.song_info_row.reload()
            AppState.app_state.update_taskbar()
            time.sleep(2)

    process = threading.Thread(target=background_processes)
    process.start()


ft.app(main, view=AppView.WEB_BROWSER, port=8550, assets_dir="assets")
