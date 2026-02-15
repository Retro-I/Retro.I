import flet as ft

from core.app_state import AppState
from core.factories.strip_factory import create_strip_state
from helper.AudioEffects import AudioEffects
from helper.BassStepsHelper import BassStepsHelper
from helper.Constants import Constants
from helper.TrebleStepsHelper import TrebleStepsHelper

audio_effects = AudioEffects()
bass_steps_helper = BassStepsHelper()
treble_steps_helper = TrebleStepsHelper()


class AudioEffectsDialog(ft.AlertDialog):
    strip_state = create_strip_state()

    def __init__(self):
        super().__init__()

        self.bass_slider = ft.Slider(
            on_change=lambda e: self.on_bass_change(),
            min=bass_steps_helper.get_min_step(),
            max=bass_steps_helper.get_max_step(),
            divisions=bass_steps_helper.get_steps_count() - 1,
            width=350,
            value=Constants.current_bass_step,
        )

        self.treble_slider = ft.Slider(
            on_change=lambda e: self.on_treble_change(),
            min=treble_steps_helper.get_min_step(),
            max=treble_steps_helper.get_max_step(),
            divisions=treble_steps_helper.get_steps_count() - 1,
            width=350,
            value=Constants.current_treble_step,
        )

        self.bass_text = ft.Text(f"{Constants.current_bass_step}")
        self.treble_text = ft.Text(f"{Constants.current_treble_step}")

        self.title = ft.Text("Bässe/Treble")
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
                        ft.Text("Treble"),
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
        self.update_content()

        self.strip_state.update_bass_strip(Constants.current_bass_step)
        AppState.app_state.update_taskbar()

    def on_treble_change(self):
        Constants.current_treble_step = int(self.treble_slider.value)
        audio_effects.update_treble(Constants.current_treble_step)
        self.update_content()

        self.strip_state.update_treble_strip(Constants.current_treble_step)
        AppState.app_state.update_taskbar()

    def open_dialog(self):
        self.update_content()
        self.open = True
        self.update()
