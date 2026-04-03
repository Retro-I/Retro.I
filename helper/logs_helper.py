import logging
import subprocess

from core.factories.helper_factories import (
    create_audio_helper,
    create_revision_helper,
    create_system_helper,
    create_theme_helper,
)
from core.factories.settings_factories import (
    create_party_mode_settings,
    create_scrollbar_settings,
    create_secured_mode_settings,
    create_strip_settings,
)
from helper.constants import Constants

logger = logging.getLogger(__name__)

system_helper = create_system_helper()
revision_helper = create_revision_helper()
secured_mode_settings_helper = create_secured_mode_settings()
audio_helper = create_audio_helper()
party_mode_helper = create_party_mode_settings()


class LogsHelper:
    def __init__(self):
        self.theme_helper = create_theme_helper()
        self.scrollbar_settings_helper = create_scrollbar_settings()
        self.strip_settings_helper = create_strip_settings()

    def get_logs(self) -> str:
        start_time = f"{Constants.get_service_start_time()}"
        logs = subprocess.check_output(
            ["journalctl", "-u", "retroi", "-S", start_time, "--no-pager"],
            text=True,
        )
        return logs

    def print_debug_infos(self):
        logger.info("")
        logger.info(" -------- Debug Informations --------")
        logger.info(f" Date: {system_helper.get_curr_date()}")
        logger.info(f" Version: {revision_helper.get_current_revision()}")
        logger.info(f" IP: {system_helper.get_ip_address()}")
        logger.info(f"     Over WIFI: {system_helper.get_current_ssid()}")
        logger.info(f"     Hostname: {system_helper.get_hostname()}")
        logger.info(f" Party-Mode: {party_mode_helper.is_party_mode()}")
        logger.info(
            f" Secured-Mode: "
            f"{secured_mode_settings_helper.is_secured_mode_enabled()}"
        )
        logger.info(f" Theme: {self.theme_helper.get_theme()}")
        logger.info(
            f" Scrollbar enalbed: "
            f"{self.scrollbar_settings_helper.is_scrollbar_enabled()}"
        )
        logger.info(f" Audio: {audio_helper.get_current_audio_sink()}")
        logger.info(f"     Volume: {audio_helper.get_volume()}")
        logger.info(f"     Default-Volume: {audio_helper.get_default_volume()}")
        logger.info(f"     Volume-Step: {audio_helper.get_volume_step()}")
        logger.info(f"     Is muted: {audio_helper.is_mute()}")
        logger.info(
            f"     Autoplay enabled: "
            f"{audio_helper.is_default_station_autoplay_enabled()}"
        )
        logger.info(" Strip")
        logger.info(
            f"     Is active: {self.strip_settings_helper.is_strip_active()}"
        )
        logger.info(
            f"     Length: {self.strip_settings_helper.get_led_length()}"
        )
        logger.info(
            f"     Brightness: "
            f"{self.strip_settings_helper.get_curr_brightness()}"
        )
        logger.info(" -------- Debug Informations --------")
        logger.info("")
