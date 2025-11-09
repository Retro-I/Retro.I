import flet as ft

from helper.Audio import Audio

audio_helper = Audio()


class VolumeDialog(ft.AlertDialog):
    def __init__(self, on_update, on_volume_update, on_mute_update):
        super().__init__()

        self.on_update = on_update
        self.on_volume_update = on_volume_update
        self.on_mute_update = on_mute_update

        self.volume_slider = ft.Slider(
            on_change=lambda e: self.on_volume_change(),
            min=0,
            max=100,
            divisions=20,
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
        self.volume_slider.disabled = audio_helper.is_mute()
        self.volume_slider.update()

        self.on_mute_update(audio_helper.is_mute())
        self.on_update()

    def on_volume_change(self):
        audio_helper.set_volume(int(self.volume_slider.value))
        self.volume_text.value = f"{audio_helper.get_volume()}%"
        self.volume_text.update()

        self.on_volume_update(int(audio_helper.get_volume()))
        self.on_update()

    def open_dialog(self):
        self.open = True
        self.update()
