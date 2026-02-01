import RPi.GPIO as GPIO

from helper.GpioHelper import GpioHelper
from helper.PartyModeHelper import PartyModeHelper
from helper.SecuredModeSettingsHelper import SecuredModeSettingsHelper

gpio_helper = GpioHelper()
party_mode_helper = PartyModeHelper()

# Hierbei handelt es sich um ein Überbleibsel aus Zeiten des Radio's des
# BSZ Wiesau, um bei offiziellen Veranstaltungen das Soundboard zu verstecken.
# Dabei muss dieses Skript in der main.py importiert werden.
# Um das Soundboard zu aktivieren, ...

GPIO.setmode(GPIO.BCM)

PIN = gpio_helper.start_party_button()

GPIO.setup(PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

secured_mode_settings_helper = SecuredModeSettingsHelper()
input_state = (
    GPIO.input(PIN)
    if secured_mode_settings_helper.is_secured_mode_enabled()
    else False
)

if not input_state:
    party_mode_helper.enable_party_mode()
