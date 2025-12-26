import json
import os

from test.base_test import BaseTest


class TestSyncValues(BaseTest):
    def setUp(self):
        super().setUp()

    def test_all_settings_files_valid(self):
        self.settings_sync_helper.validate_all_settings()

    def test_data_validation(self):
        data = {"enableAutoplay": True, "defaultVolume": 20}
        self.assertTrue(self.settings_sync_helper.is_valid(data, self._get_test_schema()))

    def test_add_volume_step_field(self):
        old_data = {"enableAutoplay": True, "defaultVolume": 20}
        schema = self.settings_sync_helper.get_schema_for_filename(
            self.audio_helper.AUDIO_SETTINGS_PATH
        )
        self.assertFalse(self.settings_sync_helper.is_valid(old_data, schema))

        new_data = self.settings_sync_helper.repair(old_data, schema)
        expected = {"enableAutoplay": True, "defaultVolume": 20, "volumeStep": 6}

        self.assertEqual(new_data, expected)
        self.assertTrue(self.settings_sync_helper.is_valid(new_data, schema))

    def test_list_data_validation(self):
        data = [
            {
                "color": "#00A1D6",
                "favorite": False,
                "id": "2a756cf7-35a4-469e-ad09-0afce7913214",
                "logo": "bayern_1.png",
                "name": "Bayern 1",
                "src": "https://dispatcher.rndfnk.com/br/br1/nbopf/mp3/mid",
            }
        ]
        self.assertTrue(self.settings_sync_helper.is_valid(data, self.get_test_list_schema()))

    def test_repair_valid_file(self):
        data = {"enableAutoplay": True, "defaultVolume": 20}
        actual = self.settings_sync_helper.repair(data, self._get_test_schema())
        self.assertCountEqual(actual, data)

    def test_repair_valid_list_file(self):
        data = [
            {
                "color": "#00A1D6",
                "favorite": False,
                "id": "2a756cf7-35a4-469e-ad09-0afce7913214",
                "logo": "bayern_1.png",
                "name": "Bayern 1",
                "src": "https://dispatcher.rndfnk.com/br/br1/nbopf/mp3/mid",
            }
        ]
        actual = self.settings_sync_helper.repair(data, self.get_test_list_schema())
        self.assertCountEqual(actual, data)

    def test_repair_invalid_file_missing_field(self):
        data = {"defaultVolume": 20}
        actual = self.settings_sync_helper.repair(data, self._get_test_schema())
        expected = {"enableAutoplay": True, "defaultVolume": 20}
        self.assertCountEqual(actual, expected)

    def test_repair_invalid_list_file(self):
        data = [
            {
                "id": "2a756cf7-35a4-469e-ad09-0afce7913214",
                "logo": "bayern_1.png",
                "name": "Bayern 1",
                "src": "https://dispatcher.rndfnk.com/br/br1/nbopf/mp3/mid",
            }
        ]
        actual = self.settings_sync_helper.repair(data, self.get_test_list_schema())
        expected = [
            {
                "color": "#00FF00",
                "favorite": False,
                "id": "2a756cf7-35a4-469e-ad09-0afce7913214",
                "logo": "bayern_1.png",
                "name": "Bayern 1",
                "src": "https://dispatcher.rndfnk.com/br/br1/nbopf/mp3/mid",
            }
        ]
        self.assertCountEqual(actual, expected)

    def test_repair_empty_file(self):
        data = {}
        actual = self.settings_sync_helper.repair(data, self._get_test_schema())
        expected = {"enableAutoplay": True, "defaultVolume": 20}
        self.assertCountEqual(actual, expected)

    def test_repair_empty_file_for_enum(self):
        data = {}
        actual = self.settings_sync_helper.repair(data, self._get_test_enum_schema())
        expected = {"theme": "light"}
        self.assertCountEqual(actual, expected)

    def test_recreate_target_settings_file(self):
        os.remove(f"{self.test_dir}/audio-settings.json")
        self.assertFalse(os.path.exists(f"{self.test_dir}/audio-settings.json"))
        self.assertTrue(os.path.exists(f"{self.test_dir_default}/audio-settings.json"))

        self.settings_sync_helper.validate_and_repair_all_settings()

        self.assertTrue(os.path.exists(f"{self.test_dir}/audio-settings.json"))
        self.assertTrue(os.path.exists(f"{self.test_dir_default}/audio-settings.json"))

        with open(f"{self.test_dir}/audio-settings.json", "r") as f:
            actual = json.load(f)

        expected = {"enableAutoplay": True, "defaultVolume": 20, "volumeStep": 6}
        self.assertCountEqual(actual, expected)

    def test_delete_target_settings_file_when_default_not_present(self):
        os.remove(f"{self.test_dir_default}/audio-settings.json")
        self.assertTrue(os.path.exists(f"{self.test_dir}/audio-settings.json"))
        self.assertFalse(os.path.exists(f"{self.test_dir_default}/audio-settings.json"))

        self.settings_sync_helper.validate_and_repair_all_settings()

        self.assertFalse(os.path.exists(f"{self.test_dir}/audio-settings.json"))
        self.assertFalse(os.path.exists(f"{self.test_dir_default}/audio-settings.json"))

    def _get_test_schema(self):
        return {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "title": "AudioSettings",
            "type": "object",
            "properties": {
                "enableAutoplay": {
                    "type": "boolean",
                    "description": (
                        "Whether the favorite station should play right after system startup"
                    ),
                    "default": True,
                },
                "defaultVolume": {
                    "type": "integer",
                    "description": "The default volume on system startup",
                    "default": 20,
                },
            },
            "required": ["enableAutoplay", "defaultVolume"],
            "additionalProperties": False,
        }

    def _get_test_enum_schema(self):
        return {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "title": "ThemeModeSettings",
            "type": "object",
            "properties": {"theme": {"enum": ["light", "dark"], "default": "light"}},
            "required": ["theme"],
            "additionalProperties": False,
        }

    def get_test_list_schema(self):
        return {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "title": "RadioStationList",
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "color": {
                        "type": "string",
                        "description": "Hex color code associated with the station (e.g., #00A1D6)",
                        "pattern": "^#([0-9A-Fa-f]{3}|[0-9A-Fa-f]{6})$",
                        "default": "#00FF00",
                    },
                    "favorite": {
                        "type": "boolean",
                        "description": "Whether the station is marked as a favorite",
                        "default": False,
                    },
                    "id": {
                        "type": "string",
                        "description": "Unique identifier (UUID)",
                        "format": "uuid",
                    },
                    "logo": {
                        "type": "string",
                        "description": "Filename or URL of the station logo",
                    },
                    "name": {
                        "type": "string",
                        "description": "Display name of the station",
                        "default": "Radiosender",
                    },
                    "src": {"type": "string", "description": "Stream source URL", "format": "uri"},
                },
                "required": ["color", "favorite", "id", "logo", "name", "src"],
                "additionalProperties": False,
            },
        }
