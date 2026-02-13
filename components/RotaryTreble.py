import threading

from pyky040 import pyky040

from core.app_state import AppState
from core.strip_factory import create_strip_state
from helper.AudioEffects import AudioEffects
from helper.Constants import Constants
from helper.GpioHelper import GpioHelper
from helper.TrebleStepsHelper import TrebleStepsHelper

audio_effects = AudioEffects()
gpio_helper = GpioHelper()
treble_steps_helper = TrebleStepsHelper()


class RotaryTreble:
    COUNTER = 0
    TREBLE_STEP = 1

    TREBLE_UP_PIN = gpio_helper.rotary_treble_up()
    TREBLE_DOWN_PIN = gpio_helper.rotary_treble_down()

    strip_state = create_strip_state()

    def __init__(self):
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
                treble_steps_helper.get_min_step()
                <= Constants.current_treble_step
                < treble_steps_helper.get_max_step()
            ):
                Constants.current_treble_step += self.TREBLE_STEP
                self.update(Constants.current_treble_step)
                self.strip_state.update_treble_strip(
                    Constants.current_treble_step
                )

            if (
                Constants.current_treble_step
                > treble_steps_helper.get_max_step()
            ):
                self.update(treble_steps_helper.get_max_step())
                self.strip_state.update_treble_strip(
                    Constants.current_treble_step
                )

        self.COUNTER += 1

    def dec_treble(self):
        if self.COUNTER % 2 == 0:
            if (
                treble_steps_helper.get_min_step()
                < Constants.current_treble_step
                <= treble_steps_helper.get_max_step()
            ):
                Constants.current_treble_step -= self.TREBLE_STEP
                self.update(Constants.current_treble_step)
                self.strip_state.update_treble_strip(
                    Constants.current_treble_step
                )

            if (
                Constants.current_treble_step
                < treble_steps_helper.get_min_step()
            ):
                self.update(treble_steps_helper.get_min_step())
                self.strip_state.update_treble_strip(
                    Constants.current_treble_step
                )

        self.COUNTER -= 1

    def update(self, step):
        audio_effects.update_treble(step)
        AppState.app_state.update_taskbar()
