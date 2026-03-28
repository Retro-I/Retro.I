from core.app_platform import AppPlatform, get_app_platform


def create_audio_helper():
    match get_app_platform():
        case AppPlatform.PI:
            from core.helpers.pi.audio import PiAudioHelper

            return PiAudioHelper()
        case _:
            from core.helpers.pi.audio import PiAudioHelper

            return PiAudioHelper()
