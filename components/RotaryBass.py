import threading

from pyky040 import pyky040

from helper.Audio import Audio
from helper.AudioEffects import AudioEffects
from helper.GpioHelper import GpioHelper

audio_helper = Audio()
audio_effects = AudioEffects()
gpio_helper = GpioHelper()


class RotaryBass:
    COUNTER = 0
    BASS_STEP = 2

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
            value = audio_effects.get_bass_value() + self.BASS_STEP
            if -20 <= value <= 20:
                self.update(value, on_taskbar_update)

            if value > 20:
                self.update(20, on_taskbar_update)
        self.COUNTER += 1

    def dec_bass_boost(self, on_taskbar_update):
        if self.COUNTER % 2 == 0:
            value = audio_effects.get_bass_value() - self.BASS_STEP
            if -20 <= value <= 20:
                self.update(value, on_taskbar_update)

            if value < -20:
                self.update(-20, on_taskbar_update)
        self.COUNTER -= 1

    def update(self, value, on_taskbar_update):
        audio_effects.update_bass(value)
        on_taskbar_update()
