from unittest.mock import MagicMock

from core.factories.settings_factories import create_developer_mode_settings
from test.base_test import BaseTest


class TestDeveloperModeHelper(BaseTest):
    def setUp(self):
        super().setUp()

    def test_is_developer_mode_active(self):
        actual = create_developer_mode_settings().is_developer_mode_active()
        self.assertFalse(actual)

        create_developer_mode_settings().toggle_developer_mode_active(
            MagicMock(control=MagicMock(value=True))
        )
        actual = create_developer_mode_settings().is_developer_mode_active()
        self.assertTrue(actual)

        create_developer_mode_settings().toggle_developer_mode_active(
            MagicMock(control=MagicMock(value=False))
        )
        actual = create_developer_mode_settings().is_developer_mode_active()
        self.assertFalse(actual)

    def test_get_complete_settings(self):
        actual = create_developer_mode_settings().get_settings()
        expected = {
            "isDeveloperModeActive": False,
        }
        self.assertEqual(actual, expected)
