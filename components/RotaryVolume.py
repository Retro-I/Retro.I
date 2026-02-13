import threading

from pyky040 import pyky040

from core.app_state import AppState
from core.strip_factory import create_strip_state
from helper.Audio import Audio
from helper.GpioHelper import GpioHelper

audio_helper = Audio()
gpio_helper = GpioHelper()


class RotaryVolume:
    COUNTER = 0
    VOLUME_UP_PIN = gpio_helper.rotary_volume_up()
    VOLUME_DOWN_PIN = gpio_helper.rotary_volume_down()
    VOLUME_MUTE_PIN = gpio_helper.rotary_volume_press()

    strip_state = create_strip_state()

    def __init__(self):
        rotary = pyky040.Encoder(
            CLK=self.VOLUME_UP_PIN,
            DT=self.VOLUME_DOWN_PIN,
            SW=self.VOLUME_MUTE_PIN,
        )
        rotary.setup(
            inc_callback=lambda e: self.inc_sound(),
            dec_callback=lambda e: self.dec_sound(),
            sw_callback=lambda: self.toggle_mute(),
        )
        rotary_thread = threading.Thread(target=rotary.watch)
        rotary_thread.start()

    def inc_sound(self):
        if self.COUNTER % 2 == 0:
            value = audio_helper.get_volume() + audio_helper.get_volume_step()
            if 0 <= value <= 100:
                self.update(value)

            if value > 100:
                self.update(100)
        self.COUNTER += 1

    def dec_sound(self):
        if self.COUNTER % 2 == 0:
            value = audio_helper.get_volume() - audio_helper.get_volume_step()
            if 0 <= value <= 100:
                self.update(value)

            if value < 0:
                self.update(0)
        self.COUNTER -= 1

    def toggle_mute(self):
        is_mute = audio_helper.toggle_mute()
        self.strip_state.toggle_mute(is_mute)
        AppState.app_state.update_taskbar()

    def update(self, value):
        if not audio_helper.is_mute():
            audio_helper.set_volume(value)
            self.strip_state.update_sound_strip(value)
            AppState.app_state.update_taskbar()
