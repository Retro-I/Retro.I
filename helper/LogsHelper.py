import logging
import subprocess

from helper.Audio import Audio
from helper.Constants import Constants
from helper.RevisionHelper import RevisionHelper
from helper.ScrollbarSettingsHelper import ScrollbarSettingsHelper
from helper.SecuredModeSettingsHelper import SecuredModeSettingsHelper
from helper.StripSettingsHelper import StripSettingsHelper
from helper.SystemHelper import SystemHelper
from helper.ThemeHelper import ThemeHelper

logger = logging.getLogger(__name__)

system_helper = SystemHelper()
revision_helper = RevisionHelper()
secured_mode_settings_helper = SecuredModeSettingsHelper()
theme_helper = ThemeHelper()
scrollbar_settings_helper = ScrollbarSettingsHelper()
audio_helper = Audio()
strip_settings_helper = StripSettingsHelper()


class LogsHelper:
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
        logger.info(f" Party-Mode: {system_helper.is_party_mode()}")
        logger.info(
            f" Secured-Mode: "
            f"{secured_mode_settings_helper.is_secured_mode_enabled()}"
        )
        logger.info(f" Theme: {theme_helper.get_theme()}")
        logger.info(
            f" Scrollbar enalbed: "
            f"{scrollbar_settings_helper.is_scrollbar_enabled()}"
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
            f"     Is active: {strip_settings_helper.is_strip_active()}"
        )
        logger.info(f"     Length: {strip_settings_helper.get_led_length()}")
        logger.info(
            f"     Brightness: {strip_settings_helper.get_curr_brightness()}"
        )
        logger.info(" -------- Debug Informations --------")
        logger.info("")
