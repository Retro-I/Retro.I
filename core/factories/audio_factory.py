from core.app_platform import AppPlatform, get_app_platform


def create_audio_state():
    match get_app_platform():
        case AppPlatform.PI:
            from hardware.pi.pi_audio_hardware import PiAudioHardware

            return PiAudioHardware()
        case AppPlatform.WEB:
            from hardware.web.web_audio_hardware import WebAudioHardware

            return WebAudioHardware()
        # Default: use PI Hardware
        case _:
            from hardware.pi.pi_audio_hardware import PiAudioHardware

            return PiAudioHardware()
