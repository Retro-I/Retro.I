from core.app_platform import AppPlatform, get_app_platform


def create_system_helper():
    match get_app_platform():
        case AppPlatform.PI:
            from core.helpers.platforms.pi.system import PiSystemHelper

            return PiSystemHelper()
        case AppPlatform.WEB:
            from core.helpers.platforms.web.system import WebSystemHelper

            return WebSystemHelper()
        # Default: use WEB
        case _:
            from core.helpers.platforms.web.system import WebSystemHelper

            return WebSystemHelper()
