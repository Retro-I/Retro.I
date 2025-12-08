import threading

from pyky040 import pyky040

from helper.Audio import Audio
from helper.AudioEffects import AudioEffects
from helper.BassStepsHelper import BassStepsHelper
from helper.Constants import Constants
from helper.GpioHelper import GpioHelper

audio_helper = Audio()
audio_effects = AudioEffects()
gpio_helper = GpioHelper()
bass_steps_helper = BassStepsHelper()


class RotaryBass:
    COUNTER = 0
    BASS_STEP = 1

    BASS_UP_PIN = gpio_helper.rotary_bass_up()
    BASS_DOWN_PIN = gpio_helper.rotary_bass_down()

    def __init__(self, on_taskbar_update):
        rotary = pyky040.Encoder(CLK=self.BASS_UP_PIN, DT=self.BASS_DOWN_PIN)
        rotary.setup(
            inc_callback=lambda e: self.inc_bass_boost(on_taskbar_update),
            dec_callback=lambda e: self.dec_bass_boost(on_taskbar_update),
        )
        rotary_thread = threading.Thread(target=rotary.watch)
        rotary_thread.start()

    def inc_bass_boost(self, on_taskbar_update):
        if self.COUNTER % 2 == 0:
            step = Constants.current_bass_step + self.BASS_STEP
            if bass_steps_helper.get_min_step() <= step <= bass_steps_helper.get_max_step():
                self.update(step, on_taskbar_update)

            if step > bass_steps_helper.get_max_step():
                self.update(bass_steps_helper.get_max_step(), on_taskbar_update)
        self.COUNTER += 1

    def dec_bass_boost(self, on_taskbar_update):
        if self.COUNTER % 2 == 0:
            step = Constants.current_bass_step - self.BASS_STEP
            if bass_steps_helper.get_min_step() <= step <= bass_steps_helper.get_max_step():
                self.update(step, on_taskbar_update)

            if step < bass_steps_helper.get_min_step():
                self.update(bass_steps_helper.get_min_step(), on_taskbar_update)
        self.COUNTER -= 1

    def update(self, step, on_taskbar_update):
        audio_effects.update_bass(step)
        on_taskbar_update()
