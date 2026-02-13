import os
from enum import StrEnum


class AppPlatform(StrEnum):
    PI = ("PI",)
    WEB = ("WEB",)


def get_app_platform() -> AppPlatform:
    return AppPlatform(os.getenv("APP_PLATFORM") or "PI")
