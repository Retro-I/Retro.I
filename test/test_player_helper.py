import os
import pathlib as pl
import shutil
import sys
import tempfile
import unittest
from unittest import mock
from unittest.mock import patch

from core.factories.helper_factories import create_player_helper
from helper.constants import Constants

constants = Constants()


class TestPlayerHelper(unittest.TestCase):
    @mock.patch.dict(sys.modules, {"alsaaudio": mock.MagicMock()})
    @mock.patch.dict(sys.modules, {"playsound3": mock.MagicMock()})
    @mock.patch.dict(sys.modules, {"cairosvg": mock.MagicMock()})
    @mock.patch.dict(sys.modules, {"numpy": mock.MagicMock()})
    @mock.patch.dict(sys.modules, {"joblib": mock.MagicMock()})
    @mock.patch.dict(sys.modules, {"sklearn.cluster": mock.MagicMock()})
    def setUp(self):
        from core.helpers.pi.audio import PiAudioHelper

        self.test_dir = tempfile.mkdtemp()

        self.audio_settings_file = os.path.join(
            "./settings/audio-settings.json"
        )

        self.audio_settings_temp_file = os.path.join(
            self.test_dir, "audio_settings_data_copy.json"
        )

        shutil.copy(self.audio_settings_file, self.audio_settings_temp_file)

        with patch.object(
            PiAudioHelper, "AUDIO_SETTINGS_PATH", self.audio_settings_temp_file
        ):
            with mock.patch.object(PiAudioHelper, "init_sound"):
                self.audio_helper = PiAudioHelper()
                self.player = create_player_helper()
                self.audio_helper.AUDIO_SETTINGS_PATH = (
                    self.audio_settings_temp_file
                )

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_startup_sound(self):
        startup = f"{constants.system_sound_path()}/startup.mp3"

        startup_sound_path = pl.Path(startup)

        self.assertEqual(
            (str(startup_sound_path), startup_sound_path.is_file()),
            (str(startup_sound_path), True),
        )

        with patch.object(self.player, "_play_sound") as mock:
            self.player.startup_sound()
            mock.assert_called_once_with(startup)

    def test_shutdown_sound(self):
        shutdown = f"{constants.system_sound_path()}/shutdown.mp3"

        shutdown_sound_path = pl.Path(shutdown)

        self.assertEqual(
            (str(shutdown_sound_path), shutdown_sound_path.is_file()),
            (str(shutdown_sound_path), True),
        )

        with patch.object(self.player, "_play_sound") as mock_play_sound:
            with patch.object(self.player, "pause") as mock_pause:
                self.player.shutdown_sound()
                mock_pause.assert_called_once()
                mock_play_sound.assert_called_once_with(shutdown)

    def test_bluetooth_connected_sound(self):
        bluetooth_connected = (
            f"{constants.system_sound_path()}/bluetooth_connected.mp3"
        )

        bluetooth_connected_sound_path = pl.Path(bluetooth_connected)

        self.assertEqual(
            (
                str(bluetooth_connected_sound_path),
                bluetooth_connected_sound_path.is_file(),
            ),
            (str(bluetooth_connected_sound_path), True),
        )

        with patch.object(self.player, "_play_sound") as mock:
            self.player.bluetooth_connected()
            mock.assert_called_once_with(bluetooth_connected)

    def test_bluetooth_disconnected_sound(self):
        bluetooth_disconnected = (
            f"{constants.system_sound_path()}/bluetooth_disconnected.mp3"
        )

        bluetooth_connected_sound_path = pl.Path(bluetooth_disconnected)

        self.assertEqual(
            (
                str(bluetooth_connected_sound_path),
                bluetooth_connected_sound_path.is_file(),
            ),
            (str(bluetooth_connected_sound_path), True),
        )

        with patch.object(self.player, "_play_sound") as mock:
            self.player.bluetooth_disconnected()
            mock.assert_called_once_with(bluetooth_disconnected)
