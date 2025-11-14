from test.base_test import BaseTest


class TestScrollbarSettings(BaseTest):
    def test_default_settings(self):
        actual = self.scrollbar_settings_helper.is_scrollbar_enabled()
        self.assertFalse(actual)

    def test_toggle_scrollbar_enabled(self):
        actual = self.scrollbar_settings_helper.is_scrollbar_enabled()
        self.assertFalse(actual)

        self.scrollbar_settings_helper.toggle_scrollbar_enabled()
        actual = self.scrollbar_settings_helper.is_scrollbar_enabled()
        self.assertTrue(actual)

        self.scrollbar_settings_helper.toggle_scrollbar_enabled()
        actual = self.scrollbar_settings_helper.is_scrollbar_enabled()
        self.assertFalse(actual)
