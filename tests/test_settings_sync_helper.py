from unittest.mock import patch
from unittest.mock import call

from tests.base_test import BaseTest


class TestSyncValues(BaseTest):
    def setUp(self):
        super().setUp()

    def test_sync_one_file(self):
        source = {"enableAutoplay": True, "defaultVolume": 20,}

        target = {"enableAutoplay": False, "defaultVolume": 55,}

        result = self.settings_sync_helper.sync_values(
            source=source, target=target, template_source=""
        )

        self.assertCountEqual(result, target)

    def test_sync_one_differed_file(self):
        source = {"enableAutoplay": True, "defaultVolume": 20, "newField": "asdf",}

        target = {"enableAutoplay": False, "defaultVolume": 55,}

        expected = {"enableAutoplay": False, "defaultVolume": 55, "newField": "asdf",}

        result = self.settings_sync_helper.sync_values(
            source=source, target=target, template_source=""
        )

        self.assertCountEqual(result, expected)

    def test_sync_differed_file_deleted_field(self):
        source = {
            "enableAutoplay": True,
        }

        target = {
            "enableAutoplay": False,
            "defaultVolume": 55,
        }

        expected = {
            "enableAutoplay": False,
        }

        result = self.settings_sync_helper.sync_values(
            source=source, target=target, template_source=""
        )

        self.assertCountEqual(result, expected)

    def test_sync_one_file_remove_and_add_field(self):
        source = {
            "enableAutoplay": True,
            "defaultVolume": 20,
            "newField": 12.99,
        }

        target = {
            "enableAutoplay": False,
            "defaultVolume": 55,
            "uselessField": "ASDF",
        }

        expected = {
            "enableAutoplay": False,
            "defaultVolume": 55,
            "newField": 12.99,
        }

        result = self.settings_sync_helper.sync_values(
            source=source, target=target, template_source=""
        )

        self.assertCountEqual(result, expected)

    def test_sync_dont_update_existing_fields(self):
        source = {
            "enableAutoplay": True,
        }

        target = {
            "enableAutoplay": False,
        }

        expected = {
            "enableAutoplay": True,
        }

        result = self.settings_sync_helper.sync_values(
            source=source, target=target, template_source=""
        )

        self.assertCountEqual(result, expected)

    def test_sync_set_not_existing_fields(self):
        source = {
            "enableAutoplay": True,
        }

        target = {
        }

        expected = {
            "enableAutoplay": True,
        }

        result = self.settings_sync_helper.sync_values(
            source=source, target=target, template_source=""
        )

        self.assertCountEqual(result, expected)

    def test_sync_differed_file_list_new_field(self):
        source = [
            {
                "id": "id123",
            }
        ]

        target = [
            {
                "id": "id123",
            }
        ]

        template_source = {
            "id": "template_id",
            "newField": "asdf",
        }

        expected = [
            {
                "id": "id123",
                "newField": "asdf",
            }
        ]

        result = self.settings_sync_helper.sync_values(
            source=source, target=target, template_source=template_source
        )

        self.assertCountEqual(result, expected)

    def test_sync_differed_file_list_remove_field(self):
        source = [
            {
                "id": "id123",
            }
        ]

        target = [
            {
                "id": "id456",
                "uselessField": "ASDF",
            }
        ]

        template_source = {
            "id": "another_cool_id",
        }

        expected = [
            {
                "id": "id456",
            }
        ]

        result = self.settings_sync_helper.sync_values(
            source=source, target=target, template_source=template_source
        )

        self.assertCountEqual(result, expected)


class TestRepairAllSettingsFiles(BaseTest):
    def setUp(self):
        super().setUp()

    def test(self):
        with patch.object(self.settings_sync_helper, "repair_settings_file") as mock:
            self.settings_sync_helper.repair_all_settings_files()
            self.assertEqual(mock.call_count, 9)
            expected_calls = [
                call("audio-settings.json"),
                call("favorite-sounds.json"),
                call("gpio-pin-mapping.json"),
                call("radio-stations.json"),
                call("scrollbar-settings.json"),
                call("secured-mode-settings.json"),
                call("startup-error.json"),
                call("strip-settings.json"),
                call("theme-mode-settings.json"),
            ]
            mock.assert_has_calls(expected_calls, any_order=False)


class TestRepairSettingsFile(BaseTest):
    def setUp(self):
        super().setUp()

    def test_existing_file(self):
        self.settings_sync_helper.repair_settings_file("audio-settings.json")

    def test_not_existing_file(self):
        self.settings_sync_helper.repair_settings_file("not-existing-setting.json")
