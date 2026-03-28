from core.app_platform import AppPlatform, get_app_platform


def create_scrollbar_settings():
    match get_app_platform():
        case AppPlatform.PI:
            from core.settings.pi.scrollbar import PiScrollbarSettings

            return PiScrollbarSettings()
        case _:
            from core.settings.pi.scrollbar import PiScrollbarSettings

            return PiScrollbarSettings()
