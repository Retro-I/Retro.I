import threading

from pyky040 import pyky040

from core.app_state import AppState
from core.factories.helper_factories import create_strip_state
from core.factories.settings_factories import (
    create_bass_settings,
    create_gpio_settings,
)
from helper.audio_effects import AudioEffects
from helper.constants import Constants

audio_effects = AudioEffects()
gpio_helper = create_gpio_settings()


class RotaryBass:
    COUNTER = 0
    BASS_STEP = 1

    BASS_UP_PIN = gpio_helper.rotary_bass_up()
    BASS_DOWN_PIN = gpio_helper.rotary_bass_down()

    def __init__(self):
        self.strip_state = create_strip_state()
        self.bass_settings = create_bass_settings()

        rotary = pyky040.Encoder(CLK=self.BASS_UP_PIN, DT=self.BASS_DOWN_PIN)
        rotary.setup(
            inc_callback=lambda e: self.inc_bass_boost(),
            dec_callback=lambda e: self.dec_bass_boost(),
        )
        rotary_thread = threading.Thread(target=rotary.watch)
        rotary_thread.start()

    def inc_bass_boost(self):
        if self.COUNTER % 2 == 0:
            if (
                self.bass_settings.get_min_step()
                <= Constants.current_bass_step
                < self.bass_settings.get_max_step()
            ):
                Constants.current_bass_step += self.BASS_STEP
                self.update(Constants.current_bass_step)
                self.strip_state.update_bass_strip(Constants.current_bass_step)

            if Constants.current_bass_step > self.bass_settings.get_max_step():
                self.update(self.bass_settings.get_max_step())
                self.strip_state.update_bass_strip(Constants.current_bass_step)

        self.COUNTER += 1

    def dec_bass_boost(self):
        if self.COUNTER % 2 == 0:
            if (
                self.bass_settings.get_min_step()
                < Constants.current_bass_step
                <= self.bass_settings.get_max_step()
            ):
                Constants.current_bass_step -= self.BASS_STEP
                self.update(Constants.current_bass_step)
                self.strip_state.update_bass_strip(Constants.current_bass_step)

            if Constants.current_bass_step < self.bass_settings.get_min_step():
                self.update(self.bass_settings.get_min_step())
                self.strip_state.update_bass_strip(Constants.current_bass_step)

        self.COUNTER -= 1

    def update(self, step):
        audio_effects.update_bass(step)
        AppState.app_state.update_taskbar()
