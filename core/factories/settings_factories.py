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


def create_bass_settings():
    match get_app_platform():
        case AppPlatform.PI:
            from core.settings.pi.bass_steps import PiBassStepsSettings

            return PiBassStepsSettings()


def create_treble_settings():
    match get_app_platform():
        case AppPlatform.PI:
            from core.settings.pi.treble_steps import PiTrebleStepsSettings

            return PiTrebleStepsSettings()


def create_developer_mode_settings():
    match get_app_platform():
        case AppPlatform.PI:
            from core.settings.pi.developer_mode import PiDeveloperModeSettings

            return PiDeveloperModeSettings()


def create_gpio_settings():
    match get_app_platform():
        case AppPlatform.PI:
            from core.settings.pi.gpio import PiGpioSettings

            return PiGpioSettings()


def create_party_mode_settings():
    match get_app_platform():
        case AppPlatform.PI:
            from core.settings.pi.party_mode import PiPartyModeSettings

            return PiPartyModeSettings()
