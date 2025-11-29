from helper.RadioHelper import RadioHelper
from test.base_test import BaseTest

radio_helper = RadioHelper()


class TestThemeHelper(BaseTest):
    def setUp(self):
        super().setUp()

    def test_get_song_info(self):
        url = "https://dispatcher.rndfnk.com/br/br1/nbopf/mp3/mid"
        song_info = radio_helper.get_song_info(url)
        self.assertIsNotNone(song_info)

    def test_empty_song_info(self):
        url = "https://google.de"
        song_info = radio_helper.get_song_info(url)
        self.assertIsNotNone(song_info)
        self.assertEqual(song_info, "")

    def test_get_song_info_all_stations(self):
        stations = self.stations.load_radio_stations()
        for station in stations:
            song_info = radio_helper.get_song_info(station["src"])
            self.assertIsNotNone(song_info)

    def test_get_stations_by_name(self):
        stations = radio_helper.get_stations_by_name("Bayern 1")
        self.assertIsNotNone(stations)
        self.assertIsNotNone(stations[0])

        self.assertIsNotNone(stations[0]["color"])
        self.assertIsNotNone(stations[0]["logo"])
        self.assertIsNotNone(stations[0]["name"])
        self.assertIsNotNone(stations[0]["src"])

    def test_get_empty_stations_list(self):
        stations = radio_helper.get_stations_by_name("ASDFASDFASDFASDF")
        self.assertIsNotNone(stations)
        self.assertEqual(stations, [])
