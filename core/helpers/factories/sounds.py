from core.app_platform import AppPlatform, get_app_platform


def create_sounds_helper():
    match get_app_platform():
        case AppPlatform.PI:
            from core.helpers.pi.sounds import PiSoundsHelper

            return PiSoundsHelper()
        case _:
            from core.helpers.pi.sounds import PiSoundsHelper

            return PiSoundsHelper()
