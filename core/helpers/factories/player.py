from core.app_platform import AppPlatform, get_app_platform


def create_player_helper():
    match get_app_platform():
        case AppPlatform.PI:
            from core.helpers.platforms.pi.player import PiPlayerHelper

            return PiPlayerHelper()
        case AppPlatform.WEB:
            from core.helpers.platforms.web.player import WebPlayerHelper

            return WebPlayerHelper()
        # Default: use WEB
        case _:
            from core.helpers.platforms.web.player import WebPlayerHelper

            return WebPlayerHelper()
