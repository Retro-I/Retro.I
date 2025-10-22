import flet as ft

from helper.SystemHelper import SystemHelper

system_helper = SystemHelper()

SCROLLBAR_SPACE = 70


def with_scrollbar_space(content: ft.Control) -> ft.Control:
    space = SCROLLBAR_SPACE
    if not system_helper.is_scrollbar_enabled():
        space = 0

    content.padding = ft.padding.only(right=space)

    return content
