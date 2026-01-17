import math

import board
import neopixel
from adafruit_led_animation.animation.pulse import Pulse
from adafruit_led_animation.color import BLACK, GREEN, RED, WHITE

from helper.Audio import Audio
from helper.BassStepsHelper import BassStepsHelper
from helper.ColorHelper import ColorHelper
from helper.Constants import Constants
from helper.StripSettingsHelper import StripSettingsHelper
from utils.WaiterProcess import WaiterProcess

c = Constants()
settings_helper = StripSettingsHelper()
bass_steps_helper = BassStepsHelper()
color_helper = ColorHelper()
audio_helper = Audio()


class Strip:
    is_active = settings_helper.is_strip_active()
    sound_mode_active = False
    curr_color = GREEN

    pixel_pin = board.D10
    pixel_num = settings_helper.get_led_length()

    pixels = neopixel.NeoPixel(pixel_pin, pixel_num, brightness=0)
    animation = Pulse(
        pixels, min_intensity=0.1, speed=0.1, period=5, color=BLACK
    )

    def __init__(self):
        if settings_helper.is_strip_active():
            self.pixels.fill(GREEN)

        self.pixels.brightness = settings_helper.get_curr_brightness() / 100
        self.pixels.show()

        self.wait_proc = WaiterProcess(self.callback)
        self.animation.color = self.curr_color

    def callback(self):
        if not settings_helper.is_strip_active():
            self.animation.fill(BLACK)
            self.pixels.fill(BLACK)
            self.pixels.show()
            return

        if not audio_helper.is_mute():
            self.sound_mode_active = True
            self.pixels.fill(self.curr_color)
            self.pixels.show()

    def update_sound_strip(self, value):
        self.sound_mode_active = False
        self.wait_proc.set_wait()

        amount_pixels = math.floor(
            settings_helper.get_led_length() * (value / 100)
        )
        self.pixels.fill(BLACK)
        if amount_pixels == 0 and value > 0:
            self.pixels[0] = GREEN

        for i in range(amount_pixels):
            self.pixels[i] = GREEN

        self.pixels.show()

    def toggle_mute(self, is_mute):
        if is_mute:
            self.animation.freeze()
            self.pixels.fill(RED)
        else:
            self.pixels.fill(self.curr_color)
            self.animation.resume()

        if settings_helper.is_strip_active():
            self.pixels.show()

    def update_bass_strip(self, value):
        def _set_step():
            if value == 0:
                return

            pixels_for_step = self._get_pixels_for_step()

            pixels_to_draw = pixels_for_step * value

            if value < 0:
                for i in range(
                    self._get_middle_of_strip() + pixels_to_draw,
                    self._get_middle_of_strip(),
                ):
                    self.pixels[i] = GREEN
            else:
                for i in range(
                    self._get_middle_of_strip(),
                    self._get_middle_of_strip() + pixels_to_draw,
                ):
                    self.pixels[i] = GREEN

        self.sound_mode_active = False
        self.wait_proc.set_wait()

        self.disable(save=False)
        _set_step()
        self._set_middle()

        self.pixels.show()

    def update_treble_strip(self, value):
        def _set_step():
            if value == 0:
                return

            pixels_for_step = self._get_pixels_for_step()

            pixels_to_draw = pixels_for_step * value

            if value < 0:
                for i in range(
                    self._get_middle_of_strip() + pixels_to_draw,
                    self._get_middle_of_strip(),
                ):
                    self.pixels[i] = GREEN
            else:
                for i in range(
                    self._get_middle_of_strip(),
                    self._get_middle_of_strip() + pixels_to_draw,
                ):
                    self.pixels[i] = GREEN

        self.sound_mode_active = False
        self.wait_proc.set_wait()

        self.disable(save=False)
        _set_step()
        self._set_middle()

        self.pixels.show()

    def _get_middle_of_strip(self) -> int:
        return settings_helper.get_led_length() // 2

    def _set_middle(self):
        middle = self._get_middle_of_strip()

        self.pixels[middle - 1] = WHITE
        self.pixels[middle] = WHITE
        self.pixels[middle + 1] = WHITE

    def _get_pixels_for_step(self) -> int:
        return (
            settings_helper.get_led_length()
            // bass_steps_helper.get_steps_count()
        )

    def update_strip(self, color):
        self.sound_mode_active = True
        strip_color = color_helper.toRgb(color)
        self.curr_color = strip_color
        self.animation.color = strip_color
        self.pixels.fill(strip_color)
        if not audio_helper.is_mute() and settings_helper.is_strip_active():
            self.pixels.show()

    def toggle_strip(self, event):
        if not event.value:
            self.animation.freeze()
            self.change_brightness(0, save=False)
            self.is_active = False
            settings_helper.update_settings(is_active=False)
        else:
            self.change_brightness(
                settings_helper.get_curr_brightness(), save=False
            )
            self.animation.resume()
            self.pixels.show()
            self.is_active = True
            settings_helper.update_settings(is_active=True)

    def change_brightness(self, value, save=True):
        self.pixels.brightness = value / 100
        if self.is_active:
            self.pixels.show()
        if save:
            settings_helper.update_settings(
                settings_helper.is_strip_active(),
                float(round(value, 2)),
            )

    def run_color_loop(self):
        while True:
            if self.is_active and self.sound_mode_active:
                self.animation.animate()

    def disable(self, save: bool = True):
        self.pixels.fill(BLACK)
        self.animation.color = BLACK
        self.animation.reset()
        if save:
            self.pixels.show()
