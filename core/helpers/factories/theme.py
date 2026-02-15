from core.app_platform import AppPlatform, get_app_platform


def create_theme_helper():
    match get_app_platform():
        case AppPlatform.PI:
            from core.helpers.platforms.pi.theme import PiThemeHelper

            return PiThemeHelper()
        case AppPlatform.WEB:
            from core.helpers.platforms.web.theme import WebThemeHelper

            return WebThemeHelper()
        # Default: use WEB
        case _:
            from core.helpers.platforms.web.theme import WebThemeHelper

            return WebThemeHelper()
