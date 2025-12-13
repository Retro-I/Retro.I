import threading

from pyky040 import pyky040

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

    taskbar = None

    def __init__(self, on_taskbar_update):
        rotary = pyky040.Encoder(CLK=self.TREBLE_UP_PIN, DT=self.TREBLE_DOWN_PIN)
        rotary.setup(
            step=self.TREBLE_STEP,
            inc_callback=lambda e: self.inc_treble(on_taskbar_update),
            dec_callback=lambda e: self.dec_treble(on_taskbar_update),
        )
        rotary_thread = threading.Thread(target=rotary.watch)
        rotary_thread.start()

    def inc_treble(self, on_taskbar_update):
        if self.COUNTER % 2 == 0:
            if (
                treble_steps_helper.get_min_step()
                <= Constants.current_treble_step
                < treble_steps_helper.get_max_step()
            ):
                Constants.current_treble_step += self.TREBLE_STEP
                self.update(Constants.current_treble_step, on_taskbar_update)

            if Constants.current_treble_step > treble_steps_helper.get_max_step():
                self.update(treble_steps_helper.get_max_step(), on_taskbar_update)
        self.COUNTER += 1

    def dec_treble(self, on_taskbar_update):
        if self.COUNTER % 2 == 0:
            if (
                treble_steps_helper.get_min_step()
                < Constants.current_treble_step
                <= treble_steps_helper.get_max_step()
            ):
                Constants.current_treble_step -= self.TREBLE_STEP
                self.update(Constants.current_treble_step, on_taskbar_update)

            if Constants.current_treble_step < treble_steps_helper.get_min_step():
                self.update(treble_steps_helper.get_min_step(), on_taskbar_update)
        self.COUNTER -= 1

    def update(self, step, on_taskbar_update):
        audio_effects.update_treble(step)
        on_taskbar_update()
