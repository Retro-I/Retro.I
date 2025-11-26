import json
from tests.base_test import BaseTest


class TestSecuredModeHelper(BaseTest):
    def test_default_settings(self):
        actual = self.secured_mode_settings.get_settings()
        expected = {
            "securedModeEnabled": True,
        }

        self.assertEqual(actual, expected)

    def test_is_secured_mode_enabled(self):
        actual = self.secured_mode_settings.is_secured_mode_enabled()
        self.assertTrue(actual)

        def disable_secured_mode():
            with open(self.secured_mode_settings.SECURED_MODE_PATH, "r+") as file:
                data = {
                    "securedModeEnabled": False,
                }
                file.seek(0)
                json.dump(data, file, indent=4)
                file.truncate()

        disable_secured_mode()

        actual = self.secured_mode_settings.is_secured_mode_enabled()
        self.assertFalse(actual)

        updated_actual_settings = self.secured_mode_settings.get_settings()
        updated_expected_settings = {
            "securedModeEnabled": False,
        }
        self.assertEqual(updated_actual_settings, updated_expected_settings)
