from test.base_test import BaseTest


class TestStartupError(BaseTest):
    def test_default_settings(self):
        actual = self.startup_error_helper.get_settings()
        expected = {
            "isStartupError": False,
            "startupErrorMessage": "",
        }

        self.assertEqual(actual, expected)

    def test_write_startup_error(self):
        self.startup_error_helper.write_startup_error("ERROR_MESSAGE")

        actual = self.startup_error_helper.get_settings()
        expected = {
            "isStartupError": True,
            "startupErrorMessage": "ERROR_MESSAGE",
        }

        self.assertEqual(actual, expected)

    def test_reset_startup_error(self):
        self.startup_error_helper.write_startup_error("ERROR_MESSAGE")
        actual = self.startup_error_helper.get_settings()
        expected = {
            "isStartupError": True,
            "startupErrorMessage": "ERROR_MESSAGE",
        }
        self.assertEqual(actual, expected)

        self.startup_error_helper.reset_startup_error()
        actual_reset = self.startup_error_helper.get_settings()
        expected_reset = {
            "isStartupError": False,
            "startupErrorMessage": "",
        }
        self.assertEqual(actual_reset, expected_reset)

    def test_is_startup_error(self):
        self.assertFalse(self.startup_error_helper.is_startup_error())
        self.startup_error_helper.write_startup_error("ERROR_MESSAGE")
        self.assertTrue(self.startup_error_helper.is_startup_error())

    def test_startup_error_message(self):
        self.assertEqual(self.startup_error_helper.startup_error(), "")
        self.startup_error_helper.write_startup_error("ERROR_MESSAGE")
        self.assertEqual(
            self.startup_error_helper.startup_error(), "ERROR_MESSAGE"
        )
