from core.app_platform import AppPlatform, get_app_platform


def create_audio_helper():
    match get_app_platform():
        case AppPlatform.PI:
            from core.helpers.pi.audio import PiAudioHelper

            return PiAudioHelper()


def create_audio_effects_helper():
    match get_app_platform():
        case AppPlatform.PI:
            from core.helpers.pi.audio_effects import PiAudioEffectsHelper

            return PiAudioEffectsHelper()


def create_bluetooth_helper():
    match get_app_platform():
        case AppPlatform.PI:
            from core.helpers.pi.bluetooth import PiBluetoothHelper

            return PiBluetoothHelper()


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
            from core.hardware.pi.strip import PiStripHardware

            return PiStripHardware()


def create_wifi_helper():
    match get_app_platform():
        case AppPlatform.PI:
            from core.helpers.pi.wifi import PiWifiHelper

            return PiWifiHelper()


def create_radio_meta_helper():
    match get_app_platform():
        case AppPlatform.PI:
            from core.helpers.pi.radio_meta import PiRadioMetaHelper

            return PiRadioMetaHelper()


def create_revision_helper():
    match get_app_platform():
        case AppPlatform.PI:
            from core.helpers.pi.revision import PiRevisionHelper

            return PiRevisionHelper()


def create_logs_helper():
    match get_app_platform():
        case AppPlatform.PI:
            from core.helpers.base.logs import BaseLogsHelper

            return BaseLogsHelper()


def create_splashscreen_helper():
    match get_app_platform():
        case AppPlatform.PI:
            from core.helpers.pi.splashscreen import PiSplashscreenHelper

            return PiSplashscreenHelper()
