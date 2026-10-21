import flet as ft

from components.image_slider import ImageSlider
from core.factories.helper_factories import create_splashscreen_helper
from helper.constants import Constants
from helper.page_state import PageState


class SplashscreenDialog(ft.AlertDialog):
    def __init__(self):
        super().__init__()
        self.splashscreen_helper = create_splashscreen_helper()

        self.image_slider = ImageSlider(images=self.get_splashscreen_images())
        self.btn_back = ft.TextButton(
            "Zurück",
            on_click=lambda e: PageState.page.pop_dialog(),
            icon=ft.Icons.ARROW_BACK,
        )
        self.loading_spinner = ft.ProgressRing(
            width=20, height=20, visible=False
        )
        self.btn_apply = ft.FilledButton(
            "Auswählen",
            on_click=lambda e: self.apply_splashscreen(),
            disabled=False,
        )

        self.title = ft.Text("Splashscreen")
        self.content = ft.Column(
            width=600,
            height=500,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[self.image_slider],
        )
        self.actions = [
            self.btn_back,
            ft.Row([self.loading_spinner, self.btn_apply], tight=True),
        ]
        self.actions_alignment = ft.MainAxisAlignment.SPACE_BETWEEN

    def get_splashscreen_images(self) -> list[ft.Image]:
        return [
            ft.Image(
                fit=ft.BoxFit.CONTAIN,
                src=f"{Constants.pwd()}/assets/splashscreen/{i}",
            )
            for i in self.splashscreen_helper.get_splashscreens()
        ]

    def apply_splashscreen(self):
        self.btn_apply.disabled = True
        self.btn_apply.content = "Wird gespeichert..."
        self.btn_apply.update()
        self.loading_spinner.visible = True
        self.loading_spinner.update()
        self.update()

        selected_image = self.splashscreen_helper.get_splashscreens()[
            self.image_slider.selected_index
        ]
        self.splashscreen_helper.update_splashscreen(selected_image)

        self.loading_spinner.visible = False
        self.loading_spinner.update()
        self.btn_apply.disabled = False
        self.btn_apply.content = "Auswählen"
        self.update()

    def open_dialog(self):
        self.open = True
        self.loading_spinner.visible = False
        self.loading_spinner.update()
        self.btn_apply.disabled = False
        self.btn_apply.content = "Auswählen"
        self.update()

    def close(self):
        self.open = False
        self.update()
