import math

import flet as ft

from helper.Audio import Audio

audio_helper = Audio()

# TODO - this is just a test yet
class BassDialog(ft.AlertDialog):
    def __init__(self, on_update, on_volume_update):
        super().__init__()

        self.on_update = on_update
        self.on_volume_update = on_volume_update

        self.volume_slider = ft.Slider(
            on_change=lambda e: self.on_volume_change(),
            min=0,
            max=100,
            divisions=20,
            width=350,
            value=audio_helper.get_volume(),
            rotate=ft.Rotate(angle=0.5 * math.pi, alignment=ft.alignment.center),
            active_color=ft.colors.ON_SURFACE,
            inactive_color=ft.colors.ON_SURFACE,
        )
        self.volume_text = ft.Text(f"{audio_helper.get_volume()}%")

        self.title = ft.Text("Bass")
        self.content = ft.Column(
            alignment=ft.MainAxisAlignment.CENTER,
            width=500,
            expand=True,
            controls=[
                self.volume_text,
                self.volume_slider,
            ],
        )

    def update_content(self):
        self.volume_slider.enabled = audio_helper.is_mute()
        self.volume_slider.update()
        self.volume_slider.value = audio_helper.get_volume()
        self.volume_slider.update()
        self.volume_text.value = f"{audio_helper.get_volume()}%"
        self.volume_text.update()

    def on_volume_change(self):
        audio_helper.set_volume(int(self.volume_slider.value))
        self.volume_text.value = f"{audio_helper.get_volume()}%"
        self.volume_text.update()

        self.on_volume_update(int(audio_helper.get_volume()))
        self.on_update()

    def open_dialog(self):
        self.open = True
        self.update()
