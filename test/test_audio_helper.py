import os
import pathlib as pl
import shutil
import sys
import tempfile
import unittest
from unittest import mock
from unittest.mock import MagicMock, patch

from core.helpers.factories.player import create_player_helper
from helper.Constants import Constants
from test.base_test import BaseTest

constants = Constants()


class TestAudioHelper(BaseTest):
    def setUp(self):
        super().setUp()

    def test_default_sound_settings(self):
        actual = self.audio_helper.get_default_sound_settings()
        expected = {
            "enableAutoplay": True,
            "defaultVolume": 20,
            "volumeStep": 6,
        }
        self.assertCountEqual(actual, expected)

    def test_get_default_volume(self):
        actual = self.audio_helper.get_default_volume()
        self.assertEqual(actual, 20)

    def test_set_default_volume(self):
        actual = self.audio_helper.get_default_volume()
        self.assertEqual(actual, 20)

        self.audio_helper.set_default_volume(50)

        actual = self.audio_helper.get_default_volume()
        self.assertEqual(actual, 50)

    def test_get_volume_step(self):
        actual = self.audio_helper.get_volume_step()
        self.assertEqual(actual, 6)

    def test_set_volume_step(self):
        actual = self.audio_helper.get_volume_step()
        self.assertEqual(actual, 6)

        self.audio_helper.set_volume_step(2)

        actual = self.audio_helper.get_volume_step()
        self.assertEqual(actual, 2)


class TestAudioSounds(unittest.TestCase):
    @mock.patch.dict(sys.modules, {"alsaaudio": mock.MagicMock()})
    @mock.patch.dict(sys.modules, {"playsound3": mock.MagicMock()})
    @mock.patch.dict(sys.modules, {"cairosvg": mock.MagicMock()})
    @mock.patch.dict(sys.modules, {"numpy": mock.MagicMock()})
    @mock.patch.dict(sys.modules, {"joblib": mock.MagicMock()})
    @mock.patch.dict(sys.modules, {"sklearn.cluster": mock.MagicMock()})
    def setUp(self):
        from helper.Audio import Audio

        self.test_dir = tempfile.mkdtemp()

        self.audio_settings_file = os.path.join(
            "./settings/audio-settings.json"
        )

        self.audio_settings_temp_file = os.path.join(
            self.test_dir, "audio_settings_data_copy.json"
        )

        shutil.copy(self.audio_settings_file, self.audio_settings_temp_file)

        with patch.object(
            Audio, "AUDIO_SETTINGS_PATH", self.audio_settings_temp_file
        ):
            with mock.patch.object(Audio, "init_sound"):
                self.audio_helper = Audio()
                self.player = create_player_helper()
                self.audio_helper.AUDIO_SETTINGS_PATH = (
                    self.audio_settings_temp_file
                )

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_audio_init(self):
        with patch.object(self.audio_helper, "unmute") as unmute_mock:
            with patch.object(self.audio_helper, "set_volume") as volume_mock:
                self.audio_helper.init_sound()
                unmute_mock.assert_called_once()
                volume_mock.assert_called_once_with(
                    self.audio_helper.get_default_volume()
                )

    def test_startup_sound(self):
        startup = f"{constants.system_sound_path()}/startup.mp3"

        startup_sound_path = pl.Path(startup)

        self.assertEqual(
            (str(startup_sound_path), startup_sound_path.is_file()),
            (str(startup_sound_path), True),
        )

        with patch.object(self.audio_helper, "play_sound") as mock:
            self.player.startup_sound()
            mock.assert_called_once_with(startup)

    def test_shutdown_sound(self):
        shutdown = f"{constants.system_sound_path()}/shutdown.mp3"

        shutdown_sound_path = pl.Path(shutdown)

        self.assertEqual(
            (str(shutdown_sound_path), shutdown_sound_path.is_file()),
            (str(shutdown_sound_path), True),
        )

        with patch.object(self.audio_helper, "play_sound") as mock_play_sound:
            with patch.object(self.audio_helper, "pause") as mock_pause:
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

        with patch.object(self.audio_helper, "play_sound") as mock:
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

        with patch.object(self.audio_helper, "play_sound") as mock:
            self.player.bluetooth_disconnected()
            mock.assert_called_once_with(bluetooth_disconnected)

        @patch("helper.Sounds.get_random_toast")
        @patch("helper.Audio.play")
        @patch("helper.Audio.wait")
        @patch("helper.Audio.pause")
        @patch("helper.Audio.playsound")
        def test_play_toast(
            mock_random_toast, mock_playsound, mock_pause, mock_wait, mock_play
        ):
            self.audio_helper.play_toast()
            mock_random_toast.assert_called_once()
            mock_pause.assert_called_once()
            mock_wait.assert_called()
            mock_playsound.assert_called_once()
            mock_play.assert_called_once()

            self.assertFalse(self.audio_helper.toast_playing)

        @patch("helper.Sounds.get_random_toast")
        @patch("helper.Audio.play")
        @patch("helper.Audio.wait")
        @patch("helper.Audio.pause")
        @patch("helper.Audio.playsound")
        def test_dont_play_toast(
            mock_random_toast, mock_playsound, mock_pause, mock_wait, mock_play
        ):
            self.audio_helper.toast_playing = True

            self.audio_helper.play_toast()
            mock_random_toast.assert_called_once()
            mock_pause.assert_not_called()
            mock_wait.assert_not_called()
            mock_playsound.assert_not_called()
            mock_play.assert_not_called()

            self.assertFalse(self.audio_helper.toast_playing)

    @mock.patch("helper.Audio.playsound")
    def test_local_sound(self, mock_playsound):
        self.audio_helper.play_sound_board("test.mp3")
        mock_playsound.assert_called_once_with(
            f"{constants.sound_path()}/test.mp3"
        )

    @mock.patch("helper.Audio.playsound")
    def test_remote_https_sound(self, mock_playsound):
        self.audio_helper.play_sound_board("https://google.de/test.mp3")
        mock_playsound.assert_called_once_with("https://google.de/test.mp3")

    @mock.patch("helper.Audio.playsound")
    def test_remote_http_sound(self, mock_playsound):
        self.audio_helper.play_sound_board("http://google.de/test.mp3")
        mock_playsound.assert_called_once_with("http://google.de/test.mp3")

    @mock.patch("time.sleep")
    def test_wait(self, mock_time_sleep):
        self.audio_helper.wait()
        mock_time_sleep.assert_called_once_with(0.5)

    @mock.patch("subprocess.run")
    def test_audio_sink_ids(self, mock_run):
        mock_run.return_value = MagicMock(stdout="""

PipeWire 'pipewire-0' [1.2.7, pi@retroi-test, cookie:3111130444]
 └─ Clients:
        33. pipewire                            [1.2.7, pi@retroi-test, pid:754]
        35. WirePlumber                         [1.2.7, pi@retroi-test, pid:753]
        36. WirePlumber [export]                [1.2.7, pi@retroi-test, pid:753]
        76. xdg-desktop-portal-wlr              [1.2.7, pi@retroi-test, pid:1119]
        77. xdg-desktop-portal                  [1.2.7, pi@retroi-test, pid:1078]
        78. unknown                             [1.2.7, pi@retroi-test, pid:1030]
        79. wpctl                               [1.2.7, pi@retroi-test, pid:17989]

Audio
 ├─ Devices:
 │      56. Built-in Audio                      [alsa]
 │      57. Built-in Audio                      [alsa]
 │      58. Built-in Audio                      [alsa]
 │
 ├─ Sinks:
 │  *   71. Built-in Audio Stereo               [vol: 0.20]
 │      72. Built-in Audio Digital Stereo (HDMI) [vol: 0.20]
 │
 ├─ Sink endpoints:
 │
 ├─ Sources:
 │
 ├─ Source endpoints:
 │
 └─ Streams:

Video
 ├─ Devices:
 │      42. rpi-hevc-dec                        [v4l2]
 │      43. bcm2835-codec-decode                [v4l2]
 │      44. bcm2835-codec-encode                [v4l2]
 │      45. bcm2835-codec-isp                   [v4l2]
 │      46. bcm2835-codec-image_fx              [v4l2]
 │      47. bcm2835-codec-encode_image          [v4l2]
 │      48. bcm2835-isp                         [v4l2]
 │      49. bcm2835-isp                         [v4l2]
 │      50. bcm2835-isp                         [v4l2]
 │      51. bcm2835-isp                         [v4l2]
 │      52. bcm2835-isp                         [v4l2]
 │      53. bcm2835-isp                         [v4l2]
 │      54. bcm2835-isp                         [v4l2]
 │      55. bcm2835-isp                         [v4l2]
 │
 ├─ Sinks:
 │
 ├─ Sink endpoints:
 │
 ├─ Sources:
 │  *   59. bcm2835-isp (V4L2)
 │      61. bcm2835-isp (V4L2)
 │      63. bcm2835-isp (V4L2)
 │      65. bcm2835-isp (V4L2)
 │
 ├─ Source endpoints:
 │
 └─ Streams:

Settings
 └─ Default Configured Node Names:
         0. Audio/Sink    alsa_output.platform-fe00b840.mailbox.stereo-fallback
        """)

        actual = self.audio_helper.get_audio_sinks()

        mock_run.assert_called_once_with(
            ["wpctl", "status"], capture_output=True, text=True, check=True
        )

        expected = [
            {
                "id": 71,
                "name": "Built-in Audio Stereo",
                "default": True,
            },
            {
                "id": 72,
                "name": "Built-in Audio Digital Stereo (HDMI)",
                "default": False,
            },
        ]
        self.assertEqual(actual, expected)

        actual_current = self.audio_helper.get_current_audio_sink()
        expected_current = {"id": 71, "name": "Built-in Audio Stereo"}
        self.assertEqual(actual_current, expected_current)
