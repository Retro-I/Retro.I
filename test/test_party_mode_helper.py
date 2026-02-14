from test.base_test import BaseTest


class TestPartyModeSettings(BaseTest):
    def test_default_settings(self):
        actual = self.party_mode_helper.get_settings()
        self.assertEqual(actual, {"isPartyMode": False})

    def test_enable_party_mode(self):
        self.party_mode_helper.enable_party_mode()
        self.assertTrue(self.party_mode_helper.is_party_mode())

        # verify
        self.party_mode_helper.enable_party_mode()
        self.assertTrue(self.party_mode_helper.is_party_mode())

    def test_disable_party_mode(self):
        self.party_mode_helper.disable_party_mode()
        self.assertFalse(self.party_mode_helper.is_party_mode())

        # verify
        self.party_mode_helper.disable_party_mode()
        self.assertFalse(self.party_mode_helper.is_party_mode())

    def test_toggle_party_mode(self):
        self.party_mode_helper.disable_party_mode()
        self.assertFalse(self.party_mode_helper.is_party_mode())

        self.party_mode_helper.toggle_party_mode()
        self.assertTrue(self.party_mode_helper.is_party_mode())

        self.party_mode_helper.toggle_party_mode()
        self.assertFalse(self.party_mode_helper.is_party_mode())
