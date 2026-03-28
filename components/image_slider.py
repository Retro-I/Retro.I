import flet as ft

from helper.SplashscreenHelper import SplashscreenHelper

splashscreen_helper = SplashscreenHelper()


class ImageSlider(ft.Container):
    selected_index = 0

    def __init__(self, images: list[ft.Image]):
        super().__init__()
        self.images = images
        self.border_radius = 12

        self.height = 600

        self.switcher_text = ft.Text("0/0", style=ft.TextStyle(size=24))

        self.switcher = ft.AnimatedSwitcher(
            images[0], duration=500, reverse_duration=500
        )
        self.content = ft.Column(
            [
                ft.Row(
                    [
                        ft.Container(
                            ft.Column([ft.Icon(ft.Icons.ARROW_LEFT, size=44)]),
                            width=36,
                            on_click=lambda e: self.prev_image(),
                        ),
                        self.switcher,
                        ft.Container(
                            ft.Column([ft.Icon(ft.Icons.ARROW_RIGHT, size=44)]),
                            width=36,
                            on_click=lambda e: self.next_image(),
                        ),
                    ],
                    expand=True,
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                ft.Row(
                    [
                        ft.Container(
                            ft.Column([self.switcher_text]),
                        ),
                    ],
                    expand=True,
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
            ],
        )

    def did_mount(self):
        self.set_current(0)

    def set_current(self, index: int):
        self.selected_index = index
        self.switcher.content = self.images[index]
        self.switcher.update()

        self.switcher_text.value = (
            f"{index + 1}/{len(splashscreen_helper.get_splashscreens())}"
        )
        self.switcher_text.update()

    def prev_image(self):
        index = self.selected_index - 1 if self.selected_index > 0 else 0
        self.set_current(index)

    def next_image(self):
        index = (
            self.selected_index + 1
            if self.selected_index
            < len(splashscreen_helper.get_splashscreens()) - 1
            else len(splashscreen_helper.get_splashscreens()) - 1
        )
        self.set_current(index)
