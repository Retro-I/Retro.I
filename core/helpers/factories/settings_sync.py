from core.app_platform import AppPlatform, get_app_platform


def create_settings_sync_helper():
    match get_app_platform():
        case AppPlatform.PI:
            from core.helpers.platforms.pi.settings_sync import (
                PiSettingsSyncHelper,
            )

            return PiSettingsSyncHelper()
        case AppPlatform.WEB:
            from core.helpers.platforms.web.settings_sync import (
                WebSettingsSyncHelper,
            )

            return WebSettingsSyncHelper()
        # Default: use WEB
        case _:
            from core.helpers.platforms.web.settings_sync import (
                WebSettingsSyncHelper,
            )

            return WebSettingsSyncHelper()
