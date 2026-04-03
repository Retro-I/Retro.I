from core.factories.helper_factories import create_radio_meta_helper
from test.base_test import BaseTest


class TestThemeHelper(BaseTest):
    def setUp(self):
        self.radio_meta_helper = create_radio_meta_helper()

        super().setUp()

    def test_get_song_info(self):
        url = "https://dispatcher.rndfnk.com/br/br1/nbopf/mp3/mid"
        song_info = self.radio_meta_helper.get_song_info(url)
        self.assertIsNotNone(song_info)

    def test_empty_song_info(self):
        url = "https://google.de"
        song_info = self.radio_meta_helper.get_song_info(url)
        self.assertIsNotNone(song_info)
        self.assertEqual(song_info, "")

    def test_get_stations_by_name(self):
        stations = self.radio_meta_helper.get_stations_by_name("Bayern 1")
        self.assertIsNotNone(stations)
        self.assertIsNotNone(stations[0])

        self.assertIsNotNone(stations[0]["color"])
        self.assertIsNotNone(stations[0]["logo"])
        self.assertIsNotNone(stations[0]["name"])
        self.assertIsNotNone(stations[0]["src"])

    def test_get_empty_stations_list(self):
        stations = self.radio_meta_helper.get_stations_by_name(
            "ASDFASDFASDFASDF"
        )
        self.assertIsNotNone(stations)
        self.assertEqual(stations, [])
