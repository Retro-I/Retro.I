import json
import math
import threading

import board
import neopixel
from adafruit_led_animation.animation.pulse import Pulse
from adafruit_led_animation.color import BLACK, GREEN, RED

from helper.ColorHelper import ColorHelper
from helper.Constants import Constants
from utils.WaiterProcess import WaiterProcess

c = Constants()


class Strip:
    STRIP_SETTINGS_PATH = f"{c.settings_path()}/strip-settings.json"

    counter = 0
    curr_color = GREEN

    color_helper = ColorHelper()

    wait_proc = WaiterProcess(None)

    def __init__(self):
        self.pixels = neopixel.NeoPixel(
            pin=board.D10, n=self.get_led_length(), brightness=0, auto_write=True
        )
        self.animation = Pulse(self.pixels, min_intensity=0.1, speed=0.1, period=5, color=BLACK)

        self.pixels.fill(GREEN)
        self.pixels.brightness = self.get_curr_brightness() / 100
        self.pixels.show()

        self.wait_proc = WaiterProcess(self.callback)
        self.animation.color = self.curr_color

    def callback(self):
        if not self.is_strip_active():
            self.animation.fill(BLACK)
        else:
            self.animation.resume()
        self.pixels.show()

    def update_sound_strip(self, value):
        self.animation.freeze()

        self.wait_proc.set_variable(value)

        amount_pixels = math.floor((self.pixel_num) * (value / 100))
        self.pixels.fill(BLACK)
        if amount_pixels == 0 and value > 0:
            self.pixels[0] = GREEN

        for i in range(amount_pixels):
            self.pixels[i] = GREEN

        self.pixels.show()

    def toggle_mute(self, is_mute):
        if self.is_strip_active():
            if is_mute:
                self.animation.freeze()
                self.pixels.fill(RED)
                self.pixels.show()
            else:
                self.pixels.fill(self.curr_color)
                self.animation.resume()
                self.pixels.show()

    def update_strip(self, color):
        self.counter = self.counter + 1

        strip_color = self.color_helper.toRgb(color)
        self.curr_color = strip_color
        self.animation.color = strip_color
        self.pixels.show()
        while self.counter <= 1:
            try:
                self.animation.animate()
            except Exception:
                pass

        self.kill_proc()

    def is_strip_active(self) -> bool:
        settings = self.get_strip_settings()
        return settings["isStripEnabled"]

    def get_led_length(self) -> int:
        settings = self.get_strip_settings()
        return settings["amountLeds"]

    def toggle_strip(self):
        if self.is_strip_active():
            self.animation.fill(BLACK)
            self.animation.freeze()
            self.update_settings(is_active=True)
        else:
            self.animation.fill(self.curr_color)
            self.animation.resume()
            self.update_settings(is_active=False)
        self.pixels.show()

    def get_curr_brightness(self) -> float:
        settings = self.get_strip_settings()
        return settings["brightness"]

    def change_brightness(self, e):
        value = e.control.value
        self.pixels.brightness = value / 100
        self.pixels.show()
        self.update_settings(brightness=float(round(value, 2)))

    def fill(self, color):
        if not self.is_strip_active():
            self.pixels.fill(color)

    def run_color(self, color):
        proc = threading.Thread(target=self.update_strip(color))
        proc.start()

    def kill_proc(self):
        self.counter -= 1

    def disable(self):
        self.pixels.fill(BLACK)
        self.animation.color = BLACK
        self.animation.reset()
        self.pixels.show()

    def get_strip_settings(self):
        with open(self.STRIP_SETTINGS_PATH) as file:
            return json.load(file)

    def update_settings(
        self, is_active: bool | None = None, brightness: float | None = None, length: int = None
    ):
        _is_active = is_active if is_active is not None else self.is_strip_active()
        _brightness = brightness if brightness is not None else self.get_curr_brightness()
        _length = length if length is not None else self.get_led_length()

        with open(self.STRIP_SETTINGS_PATH, "r+") as file:
            data = json.load(file)
            data["isStripEnabled"] = _is_active
            data["brightness"] = _brightness
            data["amountLeds"] = _length
            file.seek(0)
            json.dump(data, file, indent=4)
            file.truncate()
