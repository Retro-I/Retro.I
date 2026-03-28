from core.app_platform import AppPlatform, get_app_platform


def create_system_helper():
    match get_app_platform():
        case AppPlatform.PI:
            from core.helpers.pi.system import PiSystemHelper

            return PiSystemHelper()
        case _:
            from core.helpers.pi.system import PiSystemHelper

            return PiSystemHelper()
