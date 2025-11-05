import os
from test.base_test import BaseTest

from helper.Constants import Constants

constants = Constants()


class TestSoundsHelper(BaseTest):
    def setUp(self):
        super().setUp()

    def test_default_settings(self):
        expected = [
            {
                "id": "hog-rider-extra-loud-6366",
                "title": "hog rider extra loud",
                "url": "https://www.myinstants.com/en/instant/hog-rider-extra-loud-6366",
                "mp3": "https://www.myinstants.com/media/sounds/hog-rider-extra-loud.mp3",
            }
        ]

        actual = self.sounds_helper.load_favorite_sounds()
        self.assertEqual(expected, actual)

    def test_add_sound(self):
        sound_to_add = {
            "id": "id123",
            "title": "Was machen Sachen?",
            "url": "https://www.myinstants.com/en/instant/was-machen-sachen-123",
            "mp3": "https://www.myinstants.com/media/sounds/was-machen-sachen-123.mp3",
        }

        self.sounds_helper.add_favorite_sound(sound_to_add)

        expected = [
            {
                "id": "hog-rider-extra-loud-6366",
                "title": "hog rider extra loud",
                "url": "https://www.myinstants.com/en/instant/hog-rider-extra-loud-6366",
                "mp3": "https://www.myinstants.com/media/sounds/hog-rider-extra-loud.mp3",
            },
            {
                "id": "id123",
                "title": "Was machen Sachen?",
                "url": "https://www.myinstants.com/en/instant/was-machen-sachen-123",
                "mp3": "https://www.myinstants.com/media/sounds/was-machen-sachen-123.mp3",
            },
        ]

        actual = self.sounds_helper.load_favorite_sounds()
        self.assertEqual(expected, actual)

    def test_delete_sound(self):
        sound_to_add = {
            "id": "id123",
            "title": "Was machen Sachen?",
            "url": "https://www.myinstants.com/en/instant/was-machen-sachen-123",
            "mp3": "https://www.myinstants.com/media/sounds/was-machen-sachen-123.mp3",
        }

        expected = [
            {
                "id": "hog-rider-extra-loud-6366",
                "title": "hog rider extra loud",
                "url": "https://www.myinstants.com/en/instant/hog-rider-extra-loud-6366",
                "mp3": "https://www.myinstants.com/media/sounds/hog-rider-extra-loud.mp3",
            },
            {
                "id": "id123",
                "title": "Was machen Sachen?",
                "url": "https://www.myinstants.com/en/instant/was-machen-sachen-123",
                "mp3": "https://www.myinstants.com/media/sounds/was-machen-sachen-123.mp3",
            },
        ]

        self.sounds_helper.add_favorite_sound(sound_to_add)
        actual = self.sounds_helper.load_favorite_sounds()
        self.assertEqual(expected, actual)

        expected = [
            {
                "id": "hog-rider-extra-loud-6366",
                "title": "hog rider extra loud",
                "url": "https://www.myinstants.com/en/instant/hog-rider-extra-loud-6366",
                "mp3": "https://www.myinstants.com/media/sounds/hog-rider-extra-loud.mp3",
            }
        ]

        self.sounds_helper.delete_favorite_sound(sound_to_add)
        actual = self.sounds_helper.load_favorite_sounds()
        self.assertEqual(expected, actual)

    def test_load_toasts(self):
        os.environ["RETROI_DIR"] = "."
        expected = [
            "CapsLock Plus 6dB.mp3",
            "Duascht Plus 6dB.mp3",
            "Error Plus 6dB.mp3",
            "Flaschenbier Plus 6dB.mp3",
            "Rekursion Plus 6dB.mp3",
            "Weißbier Plus 6dB.mp3",
        ]

        actual = self.sounds_helper.load_toasts()

        self.assertCountEqual(expected, actual)

    def test_random_toast(self):
        os.environ["RETROI_DIR"] = "."

        actual = self.sounds_helper.get_random_toast()

        self.assertTrue(isinstance(actual, str))
        self.assertIn(actual, self.sounds_helper.load_toasts())
