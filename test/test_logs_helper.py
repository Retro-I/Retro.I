import unittest
from unittest.mock import patch

from helper.Constants import Constants
from helper.LogsHelper import LogsHelper

constants = Constants()


class TestStripSettingsHelper(unittest.TestCase):
    def setUp(self):
        super().setUp()
        self.logs_helper = LogsHelper()

    @patch("helper.LogsHelper.subprocess.check_output")
    @patch("helper.Constants.Constants.get_service_start_time")
    def test_logs(self, mock_time, mock_get_logs):
        mock_time.return_value = "2026-01-14 20:00:00"
        mock_get_logs.return_value = "some_nice_logs\nmore_logs\neven_more_logs"

        actual = self.logs_helper.get_logs()
        expected = "some_nice_logs\nmore_logs\neven_more_logs"
        self.assertEqual(actual, expected)

        mock_get_logs.assert_any_call(
            [
                "journalctl",
                "-u",
                "retroi",
                "-S",
                "2026-01-14 20:00:00",
                "--no-pager",
            ],
            text=True,
        )
