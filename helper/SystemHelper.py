import json
import os
import socket
import subprocess
import time
from datetime import datetime

import netifaces

from helper.Audio import Audio
from helper.Constants import Constants
from helper.PageState import PageState
from helper.Strip import Strip

audio_helper = Audio()
page_helper = PageState()
c = Constants()


class SystemHelper:
    SCROLLBAR_SETTINGS_PATH = f"{c.settings_path()}/scrollbar-settings.json"
    STARTUP_ERROR_PATH = f"{c.settings_path()}/startup-error.json"
    SECURED_MODE_ERROR_PATH = f"{c.settings_path()}/secured-mode-settings.json"

    strip = Strip()
    is_party = "0"

    def __init__(self):
        self.init_party_mode()

    def shutdown_system(self):
        audio_helper.shutdown_sound()
        self.strip.disable()
        time.sleep(3)
        os.system("sudo shutdown -h 0")

    def restart_system(self):
        audio_helper.shutdown_sound()
        self.strip.disable()
        time.sleep(3)
        os.system("sudo reboot")

    def stop_app(self):
        os.system("sudo systemctl stop retroi")

    def restart_app(self):
        os.system("sudo systemctl restart retroi")

    def startup_error(self) -> str | None:
        with open(self.STARTUP_ERROR_PATH) as file:
            file_data = json.load(file)

            if file_data["isStartupError"]:
                return file_data["startupErrorMessage"]

            return None

    def write_startup_error(self, message):
        with open(self.STARTUP_ERROR_PATH, "w") as file:
            data = {
                "isStartupError": True,
                "startupErroMessage": message,
            }

            file.write(json.dumps(data, sort_keys=True, indent=4, separators=(",", ": ")))

    def reset_startup_error(self):
        data = {"isStartupError": False, "startupErrorMessage": ""}

        with open(self.STARTUP_ERROR_PATH, "w") as file:
            file.write(json.dumps(data, sort_keys=True, indent=4, separators=(",", ": ")))

    def is_scrollbar_enabled(self) -> bool:
        with open(self.SCROLLBAR_SETTINGS_PATH) as file:
            file_data = json.load(file)
            return file_data["showScrollbar"]

    def toggle_scrollbar_enabled(self):
        data = {"showScrollbar": not self.is_scrollbar_enabled()}

        with open(self.SCROLLBAR_SETTINGS_PATH, "w") as file:
            file.write(json.dumps(data, sort_keys=True, indent=4, separators=(",", ": ")))

    def change_revision(self, revision):
        subprocess.run(
            ["bash", "scripts/update_project.sh", revision],
            capture_output=True,
            text=True,
            check=True,
        )

    def get_cpu_temp(self):
        line = subprocess.run(["vcgencmd", "measure_temp"], stdout=subprocess.PIPE).stdout.decode(
            "utf-8"
        )
        temp = line[5:].strip()
        return temp

    def get_curr_date(self):
        return datetime.today().strftime("%d.%m.%Y")

    def get_img_path(self, img_src):
        if "http" in img_src:
            return img_src

        return f"{c.pwd()}/assets/stations/{img_src}"

    def get_button_img_path(self):
        return f"{c.pwd()}/assets/buttons/SB_Green.png"

    def init_party_mode(self):
        self.is_party = os.environ.get("PARTY_MODE", "0")

    def is_party_mode(self):
        return self.is_party == "1"

    def is_secured_mode_enabled(self) -> bool:
        with open(self.SECURED_MODE_ERROR_PATH) as file:
            file_data = json.load(file)
            return file_data["securedModeEnabled"]

    def open_keyboard(self):
        self.close_keyboard()
        os.system("wvkbd-mobintl -L 230")

    def close_keyboard(self):
        os.system("pkill wvkbd-mobintl")

    def get_default_interface(self):
        if netifaces.gateways()["default"] == {}:
            return None

        return netifaces.gateways()["default"][netifaces.AF_INET][1]

    def get_current_ssid(self):
        ssid = (
            subprocess.run(["iwgetid", "-r"], stdout=subprocess.PIPE).stdout.decode("utf-8").strip()
        )
        return ssid

    def get_ip_address(self):
        ifname = self.get_default_interface()
        return "" if ifname is None else netifaces.ifaddresses(ifname)[netifaces.AF_INET][0]["addr"]

    def get_hostname(self):
        return socket.gethostname()

    def get_netmask(self):
        ifname = self.get_default_interface()
        return (
            "" if ifname is None else netifaces.ifaddresses(ifname)[netifaces.AF_INET][0]["netmask"]
        )

    def get_mac_address(self):
        ifname = self.get_default_interface()
        return "" if ifname is None else netifaces.ifaddresses(ifname)[netifaces.AF_LINK][0]["addr"]

    def get_gateway(self):
        ifname = self.get_default_interface()
        return "" if ifname is None else netifaces.gateways()["default"][netifaces.AF_INET][0]

    def get_dns_servers(self):
        dns_servers = []
        with open("/etc/resolv.conf", "r") as f:
            for line in f:
                if line.startswith("nameserver"):
                    dns_servers.append(line.strip().split()[1])
        return dns_servers

    def get_network_config(self):
        if self.get_default_interface() is None:
            return {
                "ssid": "",
                "ip": "",
                "hostname": "",
                "subnetmask": "",
                "mac_address": "",
                "gateway": "",
                "dns": ["", ""],
            }

        return {
            "ssid": self.get_current_ssid(),
            "ip": self.get_ip_address(),
            "hostname": self.get_hostname(),
            "subnetmask": self.get_netmask(),
            "mac_address": self.get_mac_address(),
            "gateway": self.get_gateway(),
            "dns": self.get_dns_servers(),
        }

    def change_screen_brightness(self, value):
        brightness = int(value / 100 * 255)
        os.system(f"sudo echo {brightness} > /sys/class/backlight/10-0045/brightness")

    def get_curr_brightness(self):
        try:
            line = subprocess.run(
                ["sudo", "cat", "/sys/class/backlight/10-0045/brightness"],
                stdout=subprocess.PIPE,
            ).stdout.decode("utf-8")
            value = int(line) / 255 * 100
            if value < 10:
                return 10

            return value
        except Exception:
            return 100
