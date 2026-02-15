from core.app_platform import AppPlatform, get_app_platform


def create_audio_helper():
    match get_app_platform():
        case AppPlatform.PI:
            from core.helpers.platforms.pi.audio import PiAudioHelper

            return PiAudioHelper()
        case AppPlatform.WEB:
            from core.helpers.platforms.web.audio import WebAudioHelper

            return WebAudioHelper()
        # Default: use WEB
        case _:
            from core.helpers.platforms.web.audio import WebAudioHelper

            return WebAudioHelper()
