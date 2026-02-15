from core.app_platform import AppPlatform, get_app_platform


def create_color_helper():
    match get_app_platform():
        case AppPlatform.PI:
            from core.helpers.platforms.pi.color import PiColorHelper

            return PiColorHelper()
        case AppPlatform.WEB:
            from core.helpers.platforms.web.color import WebColorHelper

            return WebColorHelper()
        # Default: use WEB
        case _:
            from core.helpers.platforms.web.color import WebColorHelper

            return WebColorHelper()
