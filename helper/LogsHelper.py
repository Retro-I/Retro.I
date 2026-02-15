import logging
import subprocess

from core.app_platform import get_app_platform
from core.helpers.factories.audio import create_audio_helper
from core.helpers.factories.system import create_system_helper
from core.helpers.factories.theme import create_theme_helper
from core.settings.factories.scrollbar import create_scrollbar_settings
from core.settings.factories.strip import create_strip_settings
from helper.Constants import Constants
from helper.RevisionHelper import RevisionHelper
from helper.SecuredModeSettingsHelper import SecuredModeSettingsHelper

logger = logging.getLogger(__name__)

revision_helper = RevisionHelper()
secured_mode_settings_helper = SecuredModeSettingsHelper()


class LogsHelper:
    def __init__(self):
        self.audio_state = create_audio_helper()

        self.scrollbar_settings = create_scrollbar_settings()
        self.strip_settings = create_strip_settings()

        self.system_helper = create_system_helper()
        self.theme_helper = create_theme_helper()

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
        logger.info(f" Date: {self.system_helper.get_curr_date()}")
        logger.info(f" Platform: {get_app_platform().value}")
        logger.info(f" Version: {revision_helper.get_current_revision()}")
        logger.info(f" IP: {self.system_helper.get_ip_address()}")
        logger.info(f"     Over WIFI: {self.system_helper.get_current_ssid()}")
        logger.info(f"     Hostname: {self.system_helper.get_hostname()}")
        logger.info(f" Party-Mode: {self.system_helper.is_party_mode()}")
        logger.info(
            f" Secured-Mode: "
            f"{secured_mode_settings_helper.is_secured_mode_enabled()}"
        )
        logger.info(f" Theme: {self.theme_helper.get_theme().value}")
        logger.info(
            f" Scrollbar enalbed: "
            f"{self.scrollbar_settings.is_scrollbar_enabled()}"
        )
        logger.info(f" Audio: {self.audio_state.get_current_audio_sink()}")
        logger.info(f"     Volume: {self.audio_state.get_volume()}")
        logger.info(
            f"     Default-Volume: {self.audio_state.get_default_volume()}"
        )
        logger.info(f"     Volume-Step: {self.audio_state.get_volume_step()}")
        logger.info(f"     Is muted: {self.audio_state.is_mute()}")
        logger.info(
            f"     Autoplay enabled: "
            f"{self.audio_state.is_default_station_autoplay_enabled()}"
        )
        logger.info(" Strip")
        logger.info(f"     Is active: {self.strip_settings.is_strip_active()}")
        logger.info(f"     Length: {self.strip_settings.get_led_length()}")
        logger.info(
            f"     Brightness: {self.strip_settings.get_curr_brightness()}"
        )
        logger.info(" -------- Debug Informations --------")
        logger.info("")
