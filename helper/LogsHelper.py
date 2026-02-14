import logging
import subprocess

from core.app_platform import get_app_platform
from core.factories.audio_factory import create_audio_state
from core.settings.factories.scrollbar import create_scrollbar_settings
from helper.Constants import Constants
from helper.RevisionHelper import RevisionHelper
from helper.SecuredModeSettingsHelper import SecuredModeSettingsHelper
from helper.StripSettingsHelper import StripSettingsHelper
from helper.SystemHelper import SystemHelper
from helper.ThemeHelper import ThemeHelper

logger = logging.getLogger(__name__)

system_helper = SystemHelper()
revision_helper = RevisionHelper()
secured_mode_settings_helper = SecuredModeSettingsHelper()
theme_helper = ThemeHelper()
strip_settings_helper = StripSettingsHelper()


class LogsHelper:
    def __init__(self):
        self.audio_state = create_audio_state()

        self.scrollbar_settings = create_scrollbar_settings()

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
        logger.info(f" Platform: {get_app_platform().value}")
        logger.info(f" Version: {revision_helper.get_current_revision()}")
        logger.info(f" IP: {system_helper.get_ip_address()}")
        logger.info(f"     Over WIFI: {system_helper.get_current_ssid()}")
        logger.info(f"     Hostname: {system_helper.get_hostname()}")
        logger.info(f" Party-Mode: {system_helper.is_party_mode()}")
        logger.info(
            f" Secured-Mode: "
            f"{secured_mode_settings_helper.is_secured_mode_enabled()}"
        )
        logger.info(f" Theme: {theme_helper.get_theme().value}")
        logger.info(
            f" Scrollbar enalbed: "
            f"{self.scrollbar_settings.is_scrollbar_enabled()}"
        )
        logger.info(f" Audio: {self.audio_state.get_current_audio_sink()}")
        logger.info(f"     Volume: {self.audio_state.get_volume()}")
        logger.info(f"     Default-Volume: {self.audio_state.get_default_volume()}")
        logger.info(f"     Volume-Step: {self.audio_state.get_volume_step()}")
        logger.info(f"     Is muted: {self.audio_state.is_mute()}")
        logger.info(
            f"     Autoplay enabled: "
            f"{self.audio_state.is_default_station_autoplay_enabled()}"
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
