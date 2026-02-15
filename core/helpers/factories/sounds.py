from core.app_platform import AppPlatform, get_app_platform


def create_sounds_helper():
    match get_app_platform():
        case AppPlatform.PI:
            from core.helpers.platforms.pi.sounds import PiSoundsHelper

            return PiSoundsHelper()
        case AppPlatform.WEB:
            from core.helpers.platforms.web.sounds import WebSoundsHelper

            return WebSoundsHelper()
        # Default: use WEB
        case _:
            from core.helpers.platforms.web.sounds import WebSoundsHelper

            return WebSoundsHelper()
