from core.app_platform import AppPlatform, get_app_platform


def create_strip_state():
    match get_app_platform():
        case AppPlatform.PI:
            from hardware.pi.pi_strip_hardware import PiStripHardware

            return PiStripHardware()
        case AppPlatform.WEB:
            from hardware.web.web_strip_hardware import WebStripHardware

            return WebStripHardware()
        # Default: use PI Hardware
        case _:
            from hardware.pi.pi_strip_hardware import PiStripHardware

            return PiStripHardware()
