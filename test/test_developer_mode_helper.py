from unittest.mock import MagicMock

from helper.DeveloperModeHelper import DeveloperModeHelper
from test.base_test import BaseTest


class TestDeveloperModeHelper(BaseTest):
    def setUp(self):
        super().setUp()

    def test_is_developer_mode_active(self):
        actual = DeveloperModeHelper.is_developer_mode_active()
        self.assertFalse(actual)

        DeveloperModeHelper.toggle_developer_mode_active(
            MagicMock(control=MagicMock(value=True))
        )
        actual = DeveloperModeHelper.is_developer_mode_active()
        self.assertTrue(actual)

        DeveloperModeHelper.toggle_developer_mode_active(
            MagicMock(control=MagicMock(value=False))
        )
        actual = DeveloperModeHelper.is_developer_mode_active()
        self.assertFalse(actual)

    def test_get_complete_settings(self):
        actual = DeveloperModeHelper.get_settings()
        expected = {
            "isDeveloperModeActive": False,
        }
        self.assertEqual(actual, expected)
