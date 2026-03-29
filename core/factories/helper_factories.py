from core.app_platform import AppPlatform, get_app_platform


def create_audio_helper():
    match get_app_platform():
        case AppPlatform.PI:
            from core.helpers.pi.audio import PiAudioHelper

            return PiAudioHelper()


def create_color_helper():
    match get_app_platform():
        case AppPlatform.PI:
            from core.helpers.pi.color import PiColorHelper

            return PiColorHelper()


def create_player_helper():
    match get_app_platform():
        case AppPlatform.PI:
            from core.helpers.pi.player import PiPlayerHelper

            return PiPlayerHelper()


def create_qrcode_helper():
    match get_app_platform():
        case AppPlatform.PI:
            from core.helpers.pi.qrcode import PiQrCodeHelper

            return PiQrCodeHelper()


def create_settings_sync_helper():
    match get_app_platform():
        case AppPlatform.PI:
            from core.helpers.pi.settings_sync import PiSettingsSyncHelper

            return PiSettingsSyncHelper()


def create_sounds_helper():
    match get_app_platform():
        case AppPlatform.PI:
            from core.helpers.pi.sounds import PiSoundsHelper

            return PiSoundsHelper()


def create_system_helper():
    match get_app_platform():
        case AppPlatform.PI:
            from core.helpers.pi.system import PiSystemHelper

            return PiSystemHelper()


def create_theme_helper():
    match get_app_platform():
        case AppPlatform.PI:
            from core.helpers.pi.theme import PiThemeHelper

            return PiThemeHelper()


def create_strip_state():
    match get_app_platform():
        case AppPlatform.PI:
            from hardware.pi.pi_strip_hardware import PiStripHardware

            return PiStripHardware()
