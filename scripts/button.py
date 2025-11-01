import os

import RPi.GPIO as GPIO

from helper.GpioHelper import GpioHelper
from helper.SystemHelper import SystemHelper

gpio_helper = GpioHelper()

# Hierbei handelt es sich um ein Überbleibsel aus Zeiten des Radio's des BSZ Wiesau, um bei offiziellen Veranstaltungen
# das Soundboard zu verstecken. Dabei muss dieses Skript in der main.py importiert werden.
# Um das Soundboard zu aktivieren, ...

GPIO.setmode(GPIO.BCM)

PIN = gpio_helper.start_party_button()

GPIO.setup(PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

system_helper = SystemHelper()
input_state = GPIO.input(PIN) if system_helper.is_secured_mode_enabled() else False

if not input_state:
    os.environ["PARTY_MODE"] = "1"
else:
    os.system("unset PARTY_MODE")
