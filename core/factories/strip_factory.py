from core.app_platform import AppPlatform, get_app_platform


def create_strip_state():
    match get_app_platform():
        case AppPlatform.PI:
            from hardware.pi.pi_strip_hardware import PiStripHardware

            return PiStripHardware()
        case _:
            from hardware.pi.pi_strip_hardware import PiStripHardware

            return PiStripHardware()
