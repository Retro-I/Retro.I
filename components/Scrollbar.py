import flet as ft

from helper.ScrollbarSettingsHelper import ScrollbarSettingsHelper

scrollbar_settings_helper = ScrollbarSettingsHelper()

SCROLLBAR_SPACE = 70


def with_scrollbar_space(content: ft.Control) -> ft.Control:
    space = SCROLLBAR_SPACE
    if not scrollbar_settings_helper.is_scrollbar_enabled():
        space = 0

    p = content.padding

    if isinstance(p, int):
        p = ft.padding.Padding(p, p, p, p)
    elif p is None:
        p = ft.padding.Padding(0, 0, 0, 0)

    content.padding = ft.padding.Padding(
        left=p.left, top=p.top, right=space, bottom=p.bottom
    )

    return content
