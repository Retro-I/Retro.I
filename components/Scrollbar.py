import flet as ft

from helper.ScrollbarSettingsHelper import ScrollbarSettingsHelper

scrollbar_settings_helper = ScrollbarSettingsHelper()

SCROLLBAR_SPACE = 70


def with_scrollbar_space(content: ft.Control) -> ft.Control:
    space = SCROLLBAR_SPACE
    if not scrollbar_settings_helper.is_scrollbar_enabled():
        space = 0

    content.padding = ft.padding.only(right=space)

    return content
