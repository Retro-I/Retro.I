from core.app_platform import AppPlatform, get_app_platform


def create_admin_settings():
    match get_app_platform():
        case AppPlatform.PI:
            from core.settings.pi.admin import PiAdminSettings

            return PiAdminSettings()


def create_radio_stations_settings():
    match get_app_platform():
        case AppPlatform.PI:
            from core.settings.pi.radio_stations import PiRadioStationsSettings

            return PiRadioStationsSettings()


def create_scrollbar_settings():
    match get_app_platform():
        case AppPlatform.PI:
            from core.settings.pi.scrollbar import PiScrollbarSettings

            return PiScrollbarSettings()


def create_strip_settings():
    match get_app_platform():
        case AppPlatform.PI:
            from core.settings.pi.strip import PiStripSettings

            return PiStripSettings()
