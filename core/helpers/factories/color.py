from core.app_platform import AppPlatform, get_app_platform


def create_color_helper():
    match get_app_platform():
        case AppPlatform.PI:
            from core.helpers.pi.color import PiColorHelper

            return PiColorHelper()
        case _:
            from core.helpers.pi.color import PiColorHelper

            return PiColorHelper()
