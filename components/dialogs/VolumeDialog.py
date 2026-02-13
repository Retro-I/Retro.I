import flet as ft

from core.app_state import AppState
from core.strip_factory import create_strip_state
from helper.Audio import Audio

audio_helper = Audio()


class VolumeDialog(ft.AlertDialog):
    strip_state = create_strip_state()

    def __init__(self):
        super().__init__()

        max = 100

        self.volume_slider = ft.Slider(
            on_change=lambda e: self.on_volume_change(),
            min=0,
            max=max,
            divisions=max // audio_helper.get_volume_step(),
            value=audio_helper.get_volume(),
            expand=True,
        )
        self.volume_text = ft.Text(f"{audio_helper.get_volume()}%")

        self.title = ft.Text("Lautstärke")
        self.content = ft.Column(
            alignment=ft.MainAxisAlignment.CENTER,
            width=500,
            tight=True,
            controls=[
                ft.Switch(
                    "Stummschalten",
                    label_style=ft.TextStyle(size=18),
                    on_change=lambda e: self.toggle_mute(),
                    value=audio_helper.is_mute(),
                ),
                ft.Row(
                    [
                        self.volume_slider,
                        self.volume_text,
                    ]
                ),
            ],
        )

    def update_content(self):
        self.volume_slider.enabled = audio_helper.is_mute()
        self.volume_slider.update()
        self.volume_slider.value = audio_helper.get_volume()
        self.volume_slider.update()
        self.volume_text.value = f"{audio_helper.get_volume()}%"
        self.volume_text.update()

    def toggle_mute(self):
        audio_helper.toggle_mute()
        self.update_content()

        self.strip_state.toggle_mute(audio_helper.is_mute())
        AppState.app_state.update_taskbar()

    def on_volume_change(self):
        audio_helper.set_volume(int(self.volume_slider.value))
        self.update_content()

        self.strip_state.update_sound_strip(int(audio_helper.get_volume()))
        AppState.app_state.update_taskbar()

    def open_dialog(self):
        self.open = True
        self.update()
