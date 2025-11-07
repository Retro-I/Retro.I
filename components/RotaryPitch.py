import threading

from pyky040 import pyky040

from helper.AudioEffects import AudioEffects
from helper.GpioHelper import GpioHelper

audio_effects = AudioEffects()
gpio_helper = GpioHelper()


class RotaryPitch:
    COUNTER = 0
    PITCH_STEP = 1
    PITCH_UP_PIN = gpio_helper.rotary_pitch_up()
    PITCH_DOWN_PIN = gpio_helper.rotary_pitch_down()

    taskbar = None

    def __init__(self, on_taskbar_update):
        rotary = pyky040.Encoder(CLK=self.PITCH_UP_PIN, DT=self.PITCH_DOWN_PIN)
        rotary.setup(
            step=self.PITCH_STEP,
            inc_callback=lambda e: self.inc_pitch(on_taskbar_update),
            dec_callback=lambda e: self.dec_pitch(on_taskbar_update),
        )
        rotary_thread = threading.Thread(target=rotary.watch)
        rotary_thread.start()

    def chg_callback(self, position):
        print(position)

    def inc_pitch(self, on_taskbar_update):
        if self.COUNTER % 2 == 0:
            value = audio_effects.get_pitch_value() + self.PITCH_STEP
            if -12 <= value <= 12:
                self.update(value, on_taskbar_update)

            if value > 12:
                self.update(12, on_taskbar_update)
        self.COUNTER += 1

    def dec_pitch(self, on_taskbar_update):
        if self.COUNTER % 2 == 0:
            value = audio_effects.get_pitch_value() - self.PITCH_STEP
            if -12 <= value <= 12:
                self.update(value, on_taskbar_update)

            if value < -12:
                self.update(-12, on_taskbar_update)
        self.COUNTER -= 1

    def sw_callback(self):
        pass

    def update(self, value, on_taskbar_update):
        audio_effects.update_pitch(value)
        on_taskbar_update()
