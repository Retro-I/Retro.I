import threading

from pyky040 import pyky040

from core.app_state import AppState
from core.factories.helper_factories import (
    create_audio_effects_helper,
    create_strip_state,
)
from core.factories.settings_factories import (
    create_gpio_settings,
    create_treble_settings,
)
from helper.constants import Constants

gpio_helper = create_gpio_settings()


class RotaryTreble:
    COUNTER = 0
    TREBLE_STEP = 1

    TREBLE_UP_PIN = gpio_helper.rotary_treble_up()
    TREBLE_DOWN_PIN = gpio_helper.rotary_treble_down()

    def __init__(self):
        self.strip_state = create_strip_state()
        self.treble_settings = create_treble_settings()
        self.audio_effects = create_audio_effects_helper()

        rotary = pyky040.Encoder(
            CLK=self.TREBLE_UP_PIN, DT=self.TREBLE_DOWN_PIN
        )
        rotary.setup(
            inc_callback=lambda e: self.inc_treble(),
            dec_callback=lambda e: self.dec_treble(),
        )
        rotary_thread = threading.Thread(target=rotary.watch)
        rotary_thread.start()

    def inc_treble(self):
        if self.COUNTER % 2 == 0:
            if (
                self.treble_settings.get_min_step()
                <= Constants.current_treble_step
                < self.treble_settings.get_max_step()
            ):
                Constants.current_treble_step += self.TREBLE_STEP
                self.update(Constants.current_treble_step)
                self.strip_state.update_treble_strip(
                    Constants.current_treble_step
                )

            if (
                Constants.current_treble_step
                > self.treble_settings.get_max_step()
            ):
                self.update(self.treble_settings.get_max_step())
                self.strip_state.update_treble_strip(
                    Constants.current_treble_step
                )

        self.COUNTER += 1

    def dec_treble(self):
        if self.COUNTER % 2 == 0:
            if (
                self.treble_settings.get_min_step()
                < Constants.current_treble_step
                <= self.treble_settings.get_max_step()
            ):
                Constants.current_treble_step -= self.TREBLE_STEP
                self.update(Constants.current_treble_step)
                self.strip_state.update_treble_strip(
                    Constants.current_treble_step
                )

            if (
                Constants.current_treble_step
                < self.treble_settings.get_min_step()
            ):
                self.update(self.treble_settings.get_min_step())
                self.strip_state.update_treble_strip(
                    Constants.current_treble_step
                )

        self.COUNTER -= 1

    def update(self, step):
        self.audio_effects.update_treble(step)
        AppState.app_state.update_taskbar()
