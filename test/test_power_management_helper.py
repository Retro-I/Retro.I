from datetime import datetime

from freezegun import freeze_time

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
                        "id": 0,
                        "name": "Montag",
                        "time": "00:00",
                    },
                    {
                        "enabled": False,
                        "id": 1,
                        "name": "Dienstag",
                        "time": "00:00",
                    },
                    {
                        "enabled": False,
                        "id": 2,
                        "name": "Mittwoch",
                        "time": "00:00",
                    },
                    {
                        "enabled": False,
                        "id": 3,
                        "name": "Donnerstag",
                        "time": "00:00",
                    },
                    {
                        "enabled": False,
                        "id": 4,
                        "name": "Freitag",
                        "time": "00:00",
                    },
                    {
                        "enabled": False,
                        "id": 5,
                        "name": "Samstag",
                        "time": "00:00",
                    },
                    {
                        "enabled": False,
                        "id": 6,
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
            "id": 0,
            "name": "Montag",
            "time": "11:11",
        }
        expected = [
            {
                "enabled": True,
                "id": 0,
                "name": "Montag",
                "time": "11:11",
            },
            {
                "enabled": False,
                "id": 1,
                "name": "Dienstag",
                "time": "00:00",
            },
            {
                "enabled": False,
                "id": 2,
                "name": "Mittwoch",
                "time": "00:00",
            },
            {
                "enabled": False,
                "id": 3,
                "name": "Donnerstag",
                "time": "00:00",
            },
            {
                "enabled": False,
                "id": 4,
                "name": "Freitag",
                "time": "00:00",
            },
            {
                "enabled": False,
                "id": 5,
                "name": "Samstag",
                "time": "00:00",
            },
            {
                "enabled": False,
                "id": 6,
                "name": "Sonntag",
                "time": "00:00",
            },
        ]
        self.power_management_settings.update_management_settings(new_item)
        actual = self.power_management_settings.get_management_settings()
        self.assertEqual(actual, expected)

    def test_update_management_settings_necessary_fields_only(self):
        new_item = {
            "enabled": True,
            "id": 1,
            "name": "EIN GANZ COOLER TAG MIT ANDEREM NAMEN",
            "time": "11:23",
        }
        expected = [
            {
                "enabled": False,
                "id": 0,
                "name": "Montag",
                "time": "00:00",
            },
            {
                "enabled": True,
                "id": 1,
                "name": "Dienstag",
                "time": "11:23",
            },
            {
                "enabled": False,
                "id": 2,
                "name": "Mittwoch",
                "time": "00:00",
            },
            {
                "enabled": False,
                "id": 3,
                "name": "Donnerstag",
                "time": "00:00",
            },
            {
                "enabled": False,
                "id": 4,
                "name": "Freitag",
                "time": "00:00",
            },
            {
                "enabled": False,
                "id": 5,
                "name": "Samstag",
                "time": "00:00",
            },
            {
                "enabled": False,
                "id": 6,
                "name": "Sonntag",
                "time": "00:00",
            },
        ]
        self.power_management_settings.update_management_settings(new_item)
        actual = self.power_management_settings.get_management_settings()
        self.assertEqual(actual, expected)

    @freeze_time("2026-07-05 10:00:00")
    def test_shutdown_time_enabled(self):
        """This tests, if the shutdown time is reached -> shutdown signal"""
        self.power_management_settings.enable_power_management()
        self.power_management_settings._last_shutdown_check = datetime.now()
        self.power_management_settings.update_management_settings(
            {
                "enabled": True,
                "id": 6,
                "name": "Sonntag",
                "time": "10:00",
            }
        )
        self.assertTrue(self.power_management_settings.shutdown_time_reached())

    @freeze_time("2026-07-05 10:00:00")
    def test_shutdown_time_disabled(self):
        """This tests, if the shutdown time is reached -> shutdown signal"""
        self.power_management_settings.disable_power_management()
        self.power_management_settings._last_shutdown_check = datetime.now()
        self.power_management_settings.update_management_settings(
            {
                "enabled": True,
                "id": 6,
                "name": "Sonntag",
                "time": "10:00",
            }
        )
        self.assertFalse(self.power_management_settings.shutdown_time_reached())

    @freeze_time("2026-07-05 10:00:00")
    def test_shutdown_time_after_start(self):
        """This tests, if the shutdown time is reached. But the system was
        started after the shutdown time -> no shutdown signal"""
        self.power_management_settings.enable_power_management()
        self.power_management_settings._last_shutdown_check = datetime.now()
        self.power_management_settings.update_management_settings(
            {
                "enabled": True,
                "id": "sunday",
                "name": "Sonntag",
                "time": "09:55",
            }
        )
        self.assertFalse(self.power_management_settings.shutdown_time_reached())

    @freeze_time("2026-07-05 10:00:00")
    def test_shutdown_time(self):
        """This tests, if the shutdown time is reached -> shutdown signal"""
        self.power_management_settings.enable_power_management()
        self.power_management_settings._last_shutdown_check = datetime.now()
        self.power_management_settings.update_management_settings(
            {
                "enabled": True,
                "id": 6,
                "name": "Sonntag",
                "time": "10:00",
            }
        )
        self.assertTrue(self.power_management_settings.shutdown_time_reached())

    @freeze_time("2026-07-05 10:00:00")
    def test_shutdown_time_weekday_disabled(self):
        """This tests, if the shutdown time is reached. But the weekdays
        setting is disabled"""
        self.power_management_settings.enable_power_management()
        self.power_management_settings._last_shutdown_check = datetime.now()
        self.power_management_settings.update_management_settings(
            {
                "enabled": False,
                "id": 6,
                "name": "Sonntag",
                "time": "10:00",
            }
        )
        self.assertFalse(self.power_management_settings.shutdown_time_reached())

    @freeze_time("2026-07-05 09:00:00")
    def test_shutdown_time_not_reached(self):
        """This tests, if the shutdown time is reached. But the shutdown-time
        is not reached yet"""
        self.power_management_settings.enable_power_management()
        self.power_management_settings._last_shutdown_check = datetime.now()
        self.power_management_settings.update_management_settings(
            {
                "enabled": True,
                "id": 6,
                "name": "Sonntag",
                "time": "10:00",
            }
        )
        self.assertFalse(self.power_management_settings.shutdown_time_reached())

    @freeze_time("2026-07-05 09:00:00")
    def test_shutdown_time_system_time_reached(self):
        """This tests, if the shutdown time is reached. But the shutdown-time
        is not reached yet"""
        self.power_management_settings.enable_power_management()
        self.power_management_settings.update_management_settings(
            {
                "enabled": True,
                "id": 6,
                "name": "Sonntag",
                "time": "10:00",
            }
        )
        self.assertFalse(self.power_management_settings.shutdown_time_reached())

        with freeze_time("2026-07-05 10:05:00"):
            self.assertTrue(
                self.power_management_settings.shutdown_time_reached()
            )

    @freeze_time("2026-07-05 09:00:00")
    def test_shutdown_time_reached_in_same_minute(self):
        """This tests, if the shutdown time is reached. The shutdown-time
        was reached in the same minute"""
        self.power_management_settings.enable_power_management()
        self.power_management_settings.update_management_settings(
            {
                "enabled": True,
                "id": 6,
                "name": "Sonntag",
                "time": "10:00",
            }
        )
        self.assertFalse(self.power_management_settings.shutdown_time_reached())

        with freeze_time("2026-07-05 10:00:30"):
            self.assertTrue(
                self.power_management_settings.shutdown_time_reached()
            )

    @freeze_time("2026-07-05 09:00:00")
    def test_shutdown_time_reached_in_same_second(self):
        """This tests, if the shutdown time is reached. The shutdown-time
        was reached in the same minute"""
        self.power_management_settings.enable_power_management()
        self.power_management_settings.update_management_settings(
            {
                "enabled": True,
                "id": 6,
                "name": "Sonntag",
                "time": "10:00",
            }
        )
        self.assertFalse(self.power_management_settings.shutdown_time_reached())

        with freeze_time("2026-07-05 09:59:59"):
            self.assertFalse(
                self.power_management_settings.shutdown_time_reached()
            )

        with freeze_time("2026-07-05 10:00:01"):
            self.assertTrue(
                self.power_management_settings.shutdown_time_reached()
            )
