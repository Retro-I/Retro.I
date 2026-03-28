from core.app_platform import AppPlatform, get_app_platform


def create_radio_stations_settings():
    match get_app_platform():
        case AppPlatform.PI:
            from core.settings.pi.radio_stations import PiRadioStationsSettings

            return PiRadioStationsSettings()
        case _:
            from core.settings.pi.radio_stations import PiRadioStationsSettings

            return PiRadioStationsSettings()
