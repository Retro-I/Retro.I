import logging

import flet as ft

logger = logging.getLogger(__name__)


def show_dialog(dialog):
    try:
        PageState.page.show_dialog(dialog)
    except Exception as e:
        logger.warning(e)


class PageState:
    page: ft.Page = None
