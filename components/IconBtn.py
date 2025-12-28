import flet as ft


class IconBtn(ft.Column):
    def __init__(self, text: str, icon, on_click, icon_size: int = 75):
        super().__init__()

        self.controls = [
            ft.IconButton(
                icon,
                icon_size=icon_size,
                on_click=lambda e: on_click(),
            ),
            ft.Text(
                text,
                text_align=ft.TextAlign.CENTER,
                style=ft.TextStyle(size=18),
            ),
        ]
        self.alignment = ft.MainAxisAlignment.CENTER
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER
