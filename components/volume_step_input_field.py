import flet as ft

from components.BaseTextField import BaseTextField
from helper.Audio import Audio

audio_helper = Audio()


class VolumeStepInputField(BaseTextField):
    def __init__(self):
        super().__init__()

        self.value = str(audio_helper.get_volume_step())
        self.keyboard_type = ft.KeyboardType.NUMBER
        self.input_filter = ft.InputFilter(
            allow=True,
            regex_string=r"[0-9]*",
            replacement_string="",
        )
        self.label = "Schrittweite Lautstärke"
        self.on_change = self.on_input_change

    def on_input_change(self, e):
        value = e.control.value.strip()
        error = None

        try:
            num = int(value)
            if 0 < num > 10:
                error = "Zahl muss zwischen 0 und 10 sein!"
        except ValueError:
            error = "Gib eine Zahl ein!"

        if value == "" or not value.isdigit():
            error = "Gib bitte eine Zahl ein!"

        e.control.error_text = error
        e.control.update()

        if error is None:
            audio_helper.set_volume_step(int(value))
