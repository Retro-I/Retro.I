from core.app_platform import AppPlatform, get_app_platform


def create_player_helper():
    match get_app_platform():
        case AppPlatform.PI:
            from core.helpers.pi.player import PiPlayerHelper

            return PiPlayerHelper()
        case _:
            from core.helpers.pi.player import PiPlayerHelper

            return PiPlayerHelper()
