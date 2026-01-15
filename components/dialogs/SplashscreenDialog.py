import flet as ft

from components.ImageSlider import ImageSlider
from helper.Constants import Constants
from helper.SplashscreenHelper import SplashscreenHelper

splashscreen_helper = SplashscreenHelper()


class SplashscreenDialog(ft.AlertDialog):
    def __init__(self, display_dialog):
        super().__init__()

        self.image_slider = ImageSlider(images=self.get_splashscreen_images())
        self.btn_back = ft.TextButton(
            "Zurück", on_click=lambda e: display_dialog.open_dialog(), icon=ft.Icons.ARROW_BACK
        )
        self.loading_spinner = ft.ProgressRing(width=20, height=20, visible=False)
        self.btn_apply = ft.FilledButton(
            "Auswählen", on_click=lambda e: self.apply_splashscreen(), disabled=False
        )

        self.title = ft.Text("Splashscreen")
        self.content = ft.Column(
            width=600,
            height=500,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[self.image_slider],
        )
        self.actions = [self.btn_back, ft.Row([self.loading_spinner, self.btn_apply], tight=True)]
        self.actions_alignment = ft.MainAxisAlignment.SPACE_BETWEEN

    def get_splashscreen_images(self) -> list[ft.Image]:
        return [
            ft.Image(fit=ft.ImageFit.CONTAIN, src=f"{Constants.pwd()}/assets/splashscreen/{i}")
            for i in splashscreen_helper.get_splashscreens()
        ]

    def apply_splashscreen(self):
        self.btn_apply.disabled = True
        self.btn_apply.update()
        self.loading_spinner.visible = True
        self.loading_spinner.update()
        self.btn_apply.text = "Wird gespeichert..."
        self.update()

        selected_image = splashscreen_helper.get_splashscreens()[self.image_slider.selected_index]
        splashscreen_helper.update_splashscreen(selected_image)

        self.loading_spinner.visible = False
        self.loading_spinner.update()
        self.btn_apply.disabled = False
        self.btn_apply.text = "Auswählen"
        self.update()

    def open_dialog(self):
        self.open = True
        self.loading_spinner.visible = False
        self.loading_spinner.update()
        self.btn_apply.disabled = False
        self.btn_apply.text = "Auswählen"
        self.update()

    def close(self):
        self.open = False
        self.update()
