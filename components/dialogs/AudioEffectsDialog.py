import math

import flet as ft

from components.RotaryTreble import audio_effects, treble_steps_helper
from helper.Audio import Audio
from helper.BassStepsHelper import BassStepsHelper
from helper.Constants import Constants

audio_helper = Audio()
bass_steps_helper = BassStepsHelper()


class AudioEffectsDialog(ft.AlertDialog):
    def __init__(self, on_update_bass, on_update_treble):
        super().__init__()

        self.on_update_bass = on_update_bass
        self.on_update_treble = on_update_treble

        self.bass_slider = ft.Slider(
            on_change=lambda e: self.on_bass_change(),
            min=bass_steps_helper.get_min_step(),
            max=bass_steps_helper.get_max_step(),
            divisions=bass_steps_helper.get_steps_count(),
            width=350,
            value=Constants.current_bass_step,
            active_color=ft.Colors.ON_SURFACE,
            inactive_color=ft.Colors.ON_SURFACE,
        )

        self.treble_slider = ft.Slider(
            on_change=lambda e: self.on_treble_change(),
            min=treble_steps_helper.get_min_step(),
            max=treble_steps_helper.get_max_step(),
            divisions=treble_steps_helper.get_steps_count(),
            width=350,
            value=Constants.current_treble_step,
            active_color=ft.Colors.ON_SURFACE,
            inactive_color=ft.Colors.ON_SURFACE,
        )

        self.bass_text = ft.Text(f"{Constants.current_bass_step}")
        self.treble_text = ft.Text(f"{Constants.current_treble_step}")

        self.title = ft.Text("Bässe/Höhen")
        self.content = ft.Column(
            [
                ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    expand=True,
                    controls=[
                        ft.Text("Bässe"),
                        self.bass_text,
                        self.bass_slider,
                    ],
                ),
                ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    expand=True,
                    controls=[
                        ft.Text("Höhen"),
                        self.treble_text,
                        self.treble_slider,
                    ],
                ),
            ]
        )

    def update_content(self):
        self.bass_slider.value = Constants.current_bass_step
        self.bass_slider.update()
        self.bass_text.value = f"{Constants.current_bass_step}"
        self.bass_text.update()

        self.treble_slider.value = Constants.current_treble_step
        self.treble_slider.update()
        self.treble_text.value = f"{Constants.current_treble_step}"
        self.treble_text.update()

    def on_bass_change(self):
        Constants.current_bass_step = int(self.bass_slider.value)
        audio_effects.update_bass(Constants.current_bass_step)
        self.bass_text.value = f"{Constants.current_bass_step}"
        self.bass_text.update()

        self.on_update_bass()

    def on_treble_change(self):
        Constants.current_treble_step = int(self.bass_slider.value)
        audio_effects.update_treble(Constants.current_treble_step)
        self.treble_text.value = f"{Constants.current_treble_step}"
        self.treble_text.update()

        self.on_update_treble()

    def open_dialog(self):
        self.open = True
        self.update()
