from core.app_platform import AppPlatform, get_app_platform


def create_scrollbar_settings():
    match get_app_platform():
        case AppPlatform.PI:
            from core.settings.platforms.pi.scrollbar import PiScrollbarSettings

            return PiScrollbarSettings()
        case AppPlatform.WEB:
            from core.settings.platforms.web.scrollbar import (
                WebScrollbarSettings,
            )

            return WebScrollbarSettings()
        # Default: use WEB
        case _:
            from core.settings.platforms.web.scrollbar import (
                WebScrollbarSettings,
            )

            return WebScrollbarSettings()
