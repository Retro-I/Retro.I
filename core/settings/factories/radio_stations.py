from core.app_platform import AppPlatform, get_app_platform


def create_radio_stations_settings():
    match get_app_platform():
        case AppPlatform.PI:
            from core.settings.platforms.pi.radio_stations import (
                PiRadioStationsSettings,
            )

            return PiRadioStationsSettings()
        case AppPlatform.WEB:
            from core.settings.platforms.web.radio_stations import (
                WebRadioStationsSettings,
            )

            return WebRadioStationsSettings()
        # Default: use WEB
        case _:
            from core.settings.platforms.web.radio_stations import (
                WebRadioStationsSettings,
            )

            return WebRadioStationsSettings()
