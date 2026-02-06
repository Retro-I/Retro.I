import json
import os
import re
import subprocess
import time

import alsaaudio as a
import mpv
from playsound3 import playsound

from helper.Constants import Constants
from helper.SettingsSyncHelper import SettingsSyncHelper
from helper.Sounds import Sounds

c = Constants()
sounds = Sounds()
settings_sync_helper = SettingsSyncHelper()


class Audio:
    SETTING = "audio-settings.json"
    AUDIO_SETTINGS_PATH = f"{Constants.settings_path()}/{SETTING}"

    player = mpv.MPV(ytdl=True)
    current_sound = ""
    toast_playing = False

    def __init__(self):
        home_dir = os.environ.get("HOME")
        self.mixers_path = f"{home_dir}/mixers.txt"

    def init_sound(self):
        self.unmute()
        self.set_volume(self.get_default_volume())

    def mixer(self):
        with open(self.mixers_path, "w") as f:
            f.write(str(a.mixers()))
        return a.Mixer("Master")

    def set_volume(self, value):
        if 0 <= value <= 100:
            self.mixer().setvolume(value)

    def mute(self):
        self.mixer().setmute(1)

    def unmute(self):
        self.mixer().setmute(0)

    def get_volume(self):
        return self.mixer().getvolume()[0]

    def toggle_mute(self):
        if self.is_mute():
            self.unmute()
            return False
        self.mute()
        return True

    def is_mute(self):
        return self.mixer().getmute()[0] == 1

    def play_src(self, src):
        try:
            self.pause()
        except Exception:
            print("Fehler beim abspielen des Radiosenders")
        Audio.current_sound = src
        self.play()

    def play(self):
        Audio.player.play(Audio.current_sound)

    def pause(self):
        Audio.player.stop()

    def play_sound(self, src):
        Audio.current_sound = src
        self.play()

    def startup_sound(self):
        self.play_sound(f"{c.system_sound_path()}/startup.mp3")

    def shutdown_sound(self):
        self.pause()
        self.play_sound(f"{c.system_sound_path()}/shutdown.mp3")

    def bluetooth_connected(self):
        self.play_sound(f"{c.system_sound_path()}/bluetooth_connected.mp3")

    def bluetooth_disconnected(self):
        self.play_sound(f"{c.system_sound_path()}/bluetooth_disconnected.mp3")

    def get_audio_sinks(self) -> list[dict]:
        result = subprocess.run(
            ["wpctl", "status"], capture_output=True, text=True, check=True
        )

        sinks = []
        in_sinks_section = False

        for line in result.stdout.splitlines():
            # Detect start of Audio Sinks section
            if re.search(r"Audio\s*$", line):
                continue

            if "├─ Sinks:" in line:
                in_sinks_section = True
                continue

            # Stop when leaving sinks section
            if (
                in_sinks_section
                and re.search(r"├─|└─", line)
                and "Sinks:" not in line
            ):
                break

            if in_sinks_section:
                # Matches both default (*) and non-default lines
                match = re.search(r"(\*)?\s*(\d+)\.\s+(.+?)\s+\[", line)
                if match:
                    sinks.append(
                        {
                            "id": int(match.group(2)),
                            "name": match.group(3).strip(),
                            "default": bool(match.group(1)),
                        }
                    )

        return sinks

    def get_current_audio_sink(self) -> dict:
        result = subprocess.run(
            ["wpctl", "status"], capture_output=True, text=True, check=True
        )

        in_sinks_section = False

        for line in result.stdout.splitlines():
            if "├─ Sinks:" in line:
                in_sinks_section = True
                continue

            if (
                in_sinks_section
                and re.search(r"├─|└─", line)
                and "Sinks:" not in line
            ):
                break

            if in_sinks_section:
                match = re.search(r"\*\s*(\d+)\.\s+(.+?)\s+\[", line)
                if match:
                    return {
                        "id": int(match.group(1)),
                        "name": match.group(2).strip(),
                    }

        return None

    def set_audio_output(self, sink_id: str):
        os.system(f"wpctl set-default {sink_id}")

    def play_toast(self):
        toast_src = sounds.get_random_toast()
        if not self.toast_playing:
            self.toast_playing = True
            self.pause()
            self.wait()
            self.toast = playsound(f"{c.toast_path()}/{toast_src}")
            self.wait()
            self.play()
            self.toast_playing = False

    def play_sound_board(self, src):
        if src.startswith("http"):
            playsound(src)
        else:
            playsound(f"{c.sound_path()}/{src}")

    def get_default_sound_settings(self) -> dict:
        def _get_data():
            with open(self.AUDIO_SETTINGS_PATH) as file:
                data = json.load(file)
                return data

        try:
            return _get_data()
        except Exception:
            settings_sync_helper.reset_settings_file(self.SETTING)
            return _get_data()

    def is_default_station_autoplay_enabled(self) -> bool:
        data = self.get_default_sound_settings()
        return data["enableAutoplay"]

    def toggle_default_station_autoplay(self):
        data = self.get_default_sound_settings()
        data["enableAutoplay"] = not self.is_default_station_autoplay_enabled()

        with open(self.AUDIO_SETTINGS_PATH, "r+") as file:
            file.seek(0)
            json.dump(data, file, indent=4)
            file.truncate()

    def get_default_volume(self) -> int:
        data = self.get_default_sound_settings()
        return int(data["defaultVolume"])

    def get_volume_step(self) -> int:
        data = self.get_default_sound_settings()
        return int(data["volumeStep"])

    def set_default_volume(self, volume: int):
        with open(self.AUDIO_SETTINGS_PATH, "r+") as file:
            data = json.load(file)
            data["defaultVolume"] = volume
            file.seek(0)
            json.dump(data, file, indent=4)
            file.truncate()

    def set_volume_step(self, step: int):
        with open(self.AUDIO_SETTINGS_PATH, "r+") as file:
            data = json.load(file)
            data["volumeStep"] = step
            file.seek(0)
            json.dump(data, file, indent=4)
            file.truncate()

    def wait(self):
        time.sleep(0.5)
