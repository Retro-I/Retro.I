from core.app_platform import AppPlatform, get_app_platform


def create_qrcode_helper():
    match get_app_platform():
        case AppPlatform.PI:
            from core.helpers.pi.qrcode import PiQrCodeHelper

            return PiQrCodeHelper()
        case _:
            from core.helpers.pi.qrcode import PiQrCodeHelper

            return PiQrCodeHelper()
