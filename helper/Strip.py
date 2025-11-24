import math
import threading
import time

import board
import neopixel
import math
from adafruit_led_animation.animation.pulse import Pulse
from adafruit_led_animation.color import BLACK, GREEN, RED
from helper.ColorHelper import ColorHelper
from helper.StripSettingsHelper import StripSettingsHelper
from utils.WaiterProcess import WaiterProcess
from helper.Constants import Constants

c = Constants()
settings_helper = StripSettingsHelper()
color_helper = ColorHelper()

class Strip:
    is_active = True
    sound_mode_active = False
    curr_color = GREEN

    pixel_pin = board.D10
    pixel_num = 38

    pixels = neopixel.NeoPixel(pixel_pin, pixel_num, brightness=0)
    animation = Pulse(pixels, min_intensity=0.1, speed=0.1, period=5, color=BLACK)

    def __init__(self):
        if settings_helper.is_strip_active():
            self.pixels.fill(GREEN)

        self.pixels.brightness = settings_helper.get_curr_brightness() / 100
        self.pixels.show()

        self.wait_proc = WaiterProcess(self.callback)
        self.animation.color = self.curr_color

        # TODO - find better solution
        # anim_thread = threading.Thread(target=self.run_color_loop)
        # anim_thread.start()

    def callback(self):
        if settings_helper.is_strip_active():
            self.sound_mode_active = True

            # TODO - find better solution
            self.pixels.fill(self.curr_color)
        else:
            self.animation.fill(BLACK)

            # TODO - find better solution
            self.pixels.fill(BLACK)
        self.pixels.show()

    def update_sound_strip(self, value):
        self.sound_mode_active = False
        self.wait_proc.set_wait()

        amount_pixels = math.floor(settings_helper.get_led_length() * (value / 100))
        self.pixels.fill(BLACK)
        if amount_pixels == 0 and value > 0:
            self.pixels[0] = GREEN

        for i in range(amount_pixels):
            self.pixels[i] = GREEN

        self.pixels.show()

    def toggle_mute(self, is_mute):
        if settings_helper.is_strip_active():
            if is_mute:
                self.animation.freeze()
                self.pixels.fill(RED)
            else:
                self.pixels.fill(self.curr_color)
                self.animation.resume()
                self.pixels.show()

    def update_strip(self, color):
        self.sound_mode_active = True
        strip_color = self.color_helper.toRgb(color)
        self.curr_color = strip_color
        self.animation.color = strip_color

    def toggle_strip(self):
        if settings_helper.is_strip_active():
            self.animation.freeze()
            self.change_brightness(0, save=False)
            self.is_active = False
            settings_helper.update_settings(is_active=False)
        else:
            self.change_brightness(settings_helper.get_curr_brightness(), save=False)
            self.animation.resume()
            self.pixels.show()
            self.is_active = True
            settings_helper.update_settings(is_active=True)

    def change_brightness(self, value, save=True):
        self.pixels.brightness = value / 100
        self.pixels.show()
        if save:
            settings_helper.update_settings(
                settings_helper.is_strip_active(),
                float(round(value, 2)),
            )

    def fill(self, color):
        if not settings_helper.is_strip_active():
            self.pixels.fill(color)

    def animation_loop(self):
        while True:
            if settings_helper.is_strip_active() and self.sound_mode_active:
                self.animation.animate()
            else:
                time.sleep(0.05)
            time.sleep(0.01)

    def disable(self):
        self.pixels.fill(BLACK)
        self.animation.color=BLACK
        self.animation.reset()
        self.pixels.show()