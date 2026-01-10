import flet as ft

from components.ImageSlider import ImageSlider
from helper.Constants import Constants
from helper.SplashscreenHelper import SplashscreenHelper

splashscreen_helper = SplashscreenHelper()


class SplashscreenDialog(ft.AlertDialog):
    def __init__(self):
        super().__init__()

        self.image_slider = ImageSlider(images=self.get_splashscreen_images())
        self.btn_apply = ft.FilledButton(
            "Auswählen", on_click=lambda e: self.apply_splashscreen(), disabled=False
        )

        self.content = ft.Column(
            width=600,
            expand=True,
            tight=True,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[self.image_slider],
        )
        self.actions = [self.btn_apply]
        self.actions_alignment = ft.MainAxisAlignment.END

    def get_splashscreen_images(self) -> list[ft.Image]:
        return [
            ft.Image(src=f"{Constants.pwd()}/assets/splashscreen/{i}")
            for i in splashscreen_helper.get_splashscreens()
        ]

    def apply_splashscreen(self):
        self.btn_apply.disabled = True
        self.btn_apply.text = "Wird gespeichert..."
        self.update()

        selected_image = splashscreen_helper.get_splashscreens()[self.image_slider.selected_index]
        splashscreen_helper.update_splashscreen(selected_image)

        self.btn_apply.disabled = False
        self.btn_apply.text = "Auswählen"
        self.update()

    def open_dialog(self):
        self.open = True
        self.btn_apply.disabled = False
        self.btn_apply.text = "Auswählen"
        self.update()

    def close(self):
        self.open = False
        self.update()
