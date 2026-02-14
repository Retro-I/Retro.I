import flet as ft

from core.app_state import AppState
from core.factories.audio_factory import create_audio_state
from core.factories.strip_factory import create_strip_state


class VolumeDialog(ft.AlertDialog):
    def __init__(self):
        super().__init__()

        self.strip_state = create_strip_state()
        self.audio_state = create_audio_state()

        max = 100

        self.volume_slider = ft.Slider(
            on_change=lambda e: self.on_volume_change(),
            min=0,
            max=max,
            divisions=max // self.audio_state.get_volume_step(),
            value=self.audio_state.get_volume(),
            expand=True,
        )
        self.volume_text = ft.Text(f"{self.audio_state.get_volume()}%")

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
                    value=self.audio_state.is_mute(),
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
        self.volume_slider.enabled = self.audio_state.is_mute()
        self.volume_slider.update()
        self.volume_slider.value = self.audio_state.get_volume()
        self.volume_slider.update()
        self.volume_text.value = f"{self.audio_state.get_volume()}%"
        self.volume_text.update()

    def toggle_mute(self):
        self.audio_state.toggle_mute()
        self.update_content()

        self.strip_state.toggle_mute(self.audio_state.is_mute())
        AppState.app_state.update_taskbar()

    def on_volume_change(self):
        self.audio_state.set_volume(int(self.volume_slider.value))
        self.update_content()

        self.strip_state.update_sound_strip(int(self.audio_state.get_volume()))
        AppState.app_state.update_taskbar()

    def open_dialog(self):
        self.open = True
        self.update()
