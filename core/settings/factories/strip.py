from core.app_platform import AppPlatform, get_app_platform


def create_strip_settings():
    match get_app_platform():
        case AppPlatform.PI:
            from core.settings.pi.strip import PiStripSettings

            return PiStripSettings()
        case _:
            from core.settings.pi.strip import PiStripSettings

            return PiStripSettings()
