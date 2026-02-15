from core.app_platform import AppPlatform, get_app_platform


def create_strip_settings():
    match get_app_platform():
        case AppPlatform.PI:
            from core.settings.platforms.pi.strip import PiStripSettings

            return PiStripSettings()
        case AppPlatform.WEB:
            from core.settings.platforms.web.strip import WebStripSettings

            return WebStripSettings()
        # Default: use WEB
        case _:
            from core.settings.platforms.web.strip import WebStripSettings

            return WebStripSettings()
