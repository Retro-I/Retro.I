import logging
import subprocess

from helper.Constants import Constants

logger = logging.getLogger(__name__)


class LogsHelper:
    def get_logs(self) -> str:
        start_time = f"{Constants.get_service_start_time()}"
        logs = subprocess.check_output(
            ["journalctl", "-u", "retroi", "-S", start_time, "--no-pager"],
            text=True,
        )
        return logs
