import unittest

from helper.Constants import Constants
from test.base_test import BaseTest

constants = Constants()


class TestStationsHelper(BaseTest):
    def setUp(self):
        super().setUp()

    def test_load_radio_stations(self):
        actual = self.stations.load_radio_stations()
        self.assertEqual(26, len(actual))

    # TODO - Enable and fix this with Issue #81
    @unittest.skip
    def test_add_station(self):
        station_to_add = {
            "id": "id1234",
            "favorite": False,
            "name": "Radiosender1234",
            "logo": "https://google.de/logo.png",
            "src": "station_url",
        }

        self.stations.add_station(station_to_add)
        stations = self.stations.load_radio_stations()

        self.assertIn(station_to_add, stations)

    def test_delete_station(self):
        station_to_delete = {
            "color": "#00A1D6",
            "favorite": False,
            "id": "2a756cf7-35a4-469e-ad09-0afce7913214",
            "logo": "bayern_1.png",
            "name": "Bayern 1",
            "src": "https://dispatcher.rndfnk.com/br/br1/nbopf/mp3/mid",
        }

        self.stations.delete_station(station_to_delete)

        stations = self.stations.load_radio_stations()

        self.assertEqual(25, len(stations))
        self.assertNotIn(station_to_delete, stations)

    def test_get_favorite_station(self):
        station = self.stations.get_favorite_station()
        self.assertIsNone(station)

        fav_station = self.stations.load_radio_stations()[0]
        self.stations.set_favorite_station(fav_station)

        station = self.stations.get_favorite_station()
        self.assertEqual(station, self.stations.load_radio_stations()[0])

    def test_set_favorite_station(self):
        station = self.stations.load_radio_stations()[0]

        self.stations.set_favorite_station(station)

        stations = self.stations.load_radio_stations()

        self.assertEqual(26, len(stations))
        self.assertNotIn(
            station, stations
        )  # Weil die Station anfanges `favorite=False` hatte
        self.assertTrue(stations[0]["favorite"])
        self.assertTrue(1, len([s for s in stations if s["favorite"]]))

    def test_default_station_autoplay_enabled(self):
        enabled = self.audio_helper.is_default_station_autoplay_enabled()
        self.assertTrue(enabled)

    def test_toggle_default_station_autoplay(self):
        enabled = self.audio_helper.is_default_station_autoplay_enabled()
        self.assertTrue(enabled)

        self.audio_helper.toggle_default_station_autoplay()
        enabled = self.audio_helper.is_default_station_autoplay_enabled()
        self.assertFalse(enabled)

        self.audio_helper.toggle_default_station_autoplay()
        enabled = self.audio_helper.is_default_station_autoplay_enabled()
        self.assertTrue(enabled)
