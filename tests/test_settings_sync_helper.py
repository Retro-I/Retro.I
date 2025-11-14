import unittest

from tests.base_test import BaseTest


class TestGpioHelper(BaseTest):
    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

    def test_sync_one_file(self):
        source = {
            "enableAutoplay": True,
            "defaultVolume": 20
        }

        target = {
            "enableAutoplay": False,
            "defaultVolume": 55
        }

        result = self.settings_sync_helper.sync_values(source=source, target=target, template_source="")

        self.assertCountEqual(result, target)

    def test_sync_one_differed_file(self):
        source = {
            "enableAutoplay": True,
            "defaultVolume": 20,
            "newField": "asdf"
        }

        target = {
            "enableAutoplay": False,
            "defaultVolume": 55
        }

        expected = {
            "enableAutoplay": False,
            "defaultVolume": 55,
            "newField": "asdf"
        }

        result = self.settings_sync_helper.sync_values(source=source, target=target, template_source="")

        self.assertCountEqual(result, expected)

    def test_sync_differed_file_deleted_field(self):
        source = {
            "enableAutoplay": True,
        }

        target = {
            "enableAutoplay": False,
            "defaultVolume": 55
        }

        expected = {
            "enableAutoplay": False,
        }

        result = self.settings_sync_helper.sync_values(source=source, target=target, template_source="")

        self.assertCountEqual(result, expected)

    def test_sync_differed_file_list_new_field(self):
        source = [
            {
                "id": "hog-rider-extra-loud-6366",
                "title": "hog rider extra loud",
                "url": "https://www.myinstants.com/en/instant/hog-rider-extra-loud-6366",
                "mp3": "https://www.myinstants.com/media/sounds/hog-rider-extra-loud.mp3"
            }
        ]

        target = [
            {
                "id": "hog-rider-extra-loud-6366",
                "title": "hog rider extra loud",
                "url": "https://www.myinstants.com/en/instant/hog-rider-extra-loud-6366",
                "mp3": "https://www.myinstants.com/media/sounds/hog-rider-extra-loud.mp3"
            }
        ]

        template_source = {
            "id": "hog-rider-extra-loud-6366",
            "title": "hog rider extra loud",
            "url": "https://www.myinstants.com/en/instant/hog-rider-extra-loud-6366",
            "mp3": "https://www.myinstants.com/media/sounds/hog-rider-extra-loud.mp3",
            "newField": "asdf"
        }

        expected = [
            {
                "id": "hog-rider-extra-loud-6366",
                "title": "hog rider extra loud",
                "url": "https://www.myinstants.com/en/instant/hog-rider-extra-loud-6366",
                "mp3": "https://www.myinstants.com/media/sounds/hog-rider-extra-loud.mp3",
                "newField": "asdf"
            }
        ]

        result = self.settings_sync_helper.sync_values(source=source, target=target, template_source=template_source)

        self.assertCountEqual(result, expected)

    def test_sync_differed_file_list_remove_field(self):
        source = [
            {
                "id": "hog-rider-extra-loud-6366",
                "title": "hog rider extra loud",
                "url": "https://www.myinstants.com/en/instant/hog-rider-extra-loud-6366",
                "mp3": "https://www.myinstants.com/media/sounds/hog-rider-extra-loud.mp3"
            }
        ]

        target = [
            {
                "id": "hog-rider-extra-loud-6366",
                "title": "hog rider extra loud",
                "url": "https://www.myinstants.com/en/instant/hog-rider-extra-loud-6366",
                "mp3": "https://www.myinstants.com/media/sounds/hog-rider-extra-loud.mp3",
                "uselessField": "ASDF"
            }
        ]

        template_source = {
            "id": "hog-rider-extra-loud-6366",
            "title": "hog rider extra loud",
            "url": "https://www.myinstants.com/en/instant/hog-rider-extra-loud-6366",
            "mp3": "https://www.myinstants.com/media/sounds/hog-rider-extra-loud.mp3"
        }

        expected = [
            {
                "id": "hog-rider-extra-loud-6366",
                "title": "hog rider extra loud",
                "url": "https://www.myinstants.com/en/instant/hog-rider-extra-loud-6366",
                "mp3": "https://www.myinstants.com/media/sounds/hog-rider-extra-loud.mp3"
            }
        ]

        result = self.settings_sync_helper.sync_values(source=source, target=target, template_source=template_source)

        self.assertCountEqual(result, expected)

# TODO - Testfälle vereinfachen
# TODO - Testfälle für andere Variationen überlegen und implementieren
