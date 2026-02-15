from core.app_platform import AppPlatform, get_app_platform


def create_qrcode_helper():
    match get_app_platform():
        case AppPlatform.PI:
            from core.helpers.platforms.pi.qrcode import PiQrCodeHelper

            return PiQrCodeHelper
        case AppPlatform.WEB:
            from core.helpers.platforms.web.qrcode import WebQrCodeHelper

            return WebQrCodeHelper()
        # Default: use WEB
        case _:
            from core.helpers.platforms.web.qrcode import WebQrCodeHelper

            return WebQrCodeHelper()
