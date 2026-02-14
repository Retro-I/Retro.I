import threading
import time

import flet as ft
from flet.core.types import AppView

from components.view.Theme import Theme
from core.app_state import AppState
from helper.PageState import PageState
from helper.ThemeHelper import ThemeHelper

theme_helper = ThemeHelper()


def main(page: ft.Page):
    AppState()

    page.theme_mode = theme_helper.get_theme()
    page.update()

    PageState.page = page

    theme = Theme()

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


ft.app(main, view=AppView.WEB_BROWSER, assets_dir="assets")
