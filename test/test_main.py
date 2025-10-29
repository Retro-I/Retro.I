# test_main.py
import sys
import types

# List of hardware-specific packages to mock
for module_name in [
    "RPi.GPIO",
    "pyky040",
    "rpi_rotary_encoder",
    "adafruit_neopixel",
    "adafruit_led_animation",
    "netifaces",
    "alsaaudio",
]:
    sys.modules[module_name] = types.ModuleType(module_name)

sys.modules['vlc'] = types.ModuleType('vlc')
vlc = sys.modules['vlc']
vlc.Instance = lambda *args, **kwargs: vlc
vlc.media_player_new = lambda: vlc
vlc.Media = lambda path: None
vlc.play = lambda: None
vlc.stop = lambda: None

import flet as ft
from main import main  # now safe to import

ft.app(target=main, view=ft.WEB_BROWSER, port=8550)