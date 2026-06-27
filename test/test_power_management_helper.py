from test.base_test import BaseTest


class TestPowerManagementSettings(BaseTest):
    def test_default_settings(self):
        actual = self.power_management_settings.get_settings()
        self.assertEqual(
            actual,
            {
                "enabled": False,
                "items": [
                    {
                        "enabled": False,
                        "id": "monday",
                        "name": "Montag",
                        "time": "00:00",
                    },
                    {
                        "enabled": False,
                        "id": "tuesday",
                        "name": "Dienstag",
                        "time": "00:00",
                    },
                    {
                        "enabled": False,
                        "id": "wednesday",
                        "name": "Mittwoch",
                        "time": "00:00",
                    },
                    {
                        "enabled": False,
                        "id": "thursday",
                        "name": "Donnerstag",
                        "time": "00:00",
                    },
                    {
                        "enabled": False,
                        "id": "friday",
                        "name": "Freitag",
                        "time": "00:00",
                    },
                    {
                        "enabled": False,
                        "id": "saturday",
                        "name": "Samstag",
                        "time": "00:00",
                    },
                    {
                        "enabled": False,
                        "id": "sunday",
                        "name": "Sonntag",
                        "time": "00:00",
                    },
                ],
            },
        )

    def test_enable_power_management(self):
        self.power_management_settings.enable_power_management()
        self.assertTrue(self.power_management_settings.is_enabled())

    def test_disable_power_management(self):
        self.power_management_settings.disable_power_management()
        self.assertFalse(self.power_management_settings.is_enabled())

    def test_update_management_settings(self):
        new_item = {
            "enabled": True,
            "id": "monday",
            "name": "Montag",
            "time": "11:11",
        }
        expected = [
            {
                "enabled": True,
                "id": "monday",
                "name": "Montag",
                "time": "11:11",
            },
            {
                "enabled": False,
                "id": "tuesday",
                "name": "Dienstag",
                "time": "00:00",
            },
            {
                "enabled": False,
                "id": "wednesday",
                "name": "Mittwoch",
                "time": "00:00",
            },
            {
                "enabled": False,
                "id": "thursday",
                "name": "Donnerstag",
                "time": "00:00",
            },
            {
                "enabled": False,
                "id": "friday",
                "name": "Freitag",
                "time": "00:00",
            },
            {
                "enabled": False,
                "id": "saturday",
                "name": "Samstag",
                "time": "00:00",
            },
            {
                "enabled": False,
                "id": "sunday",
                "name": "Sonntag",
                "time": "00:00",
            },
        ],
        self.power_management_settings.update_management_settings(new_item)
        actual = self.power_management_settings.get_management_settings()
        self.assertEqual(actual, expected)

    def test_update_management_settings_necessary_fields_only(self):
        new_item = {
            "enabled": True,
            "id": "tuesday",
            "name": "EIN GANZ COOLER TAG MIT ANDEREM NAMEN",
            "time": "11:23",
        }
        expected = [
            {
                "enabled": False,
                "id": "monday",
                "name": "Montag",
                "time": "00:00",
            },
            {
                "enabled": True,
                "id": "tuesday",
                "name": "Dienstag",
                "time": "11:23",
            },
            {
                "enabled": False,
                "id": "wednesday",
                "name": "Mittwoch",
                "time": "00:00",
            },
            {
                "enabled": False,
                "id": "thursday",
                "name": "Donnerstag",
                "time": "00:00",
            },
            {
                "enabled": False,
                "id": "friday",
                "name": "Freitag",
                "time": "00:00",
            },
            {
                "enabled": False,
                "id": "saturday",
                "name": "Samstag",
                "time": "00:00",
            },
            {
                "enabled": False,
                "id": "sunday",
                "name": "Sonntag",
                "time": "00:00",
            },
        ]
        self.power_management_settings.update_management_settings(new_item)
        actual = self.power_management_settings.get_management_settings()
        self.assertEqual(actual, expected)
