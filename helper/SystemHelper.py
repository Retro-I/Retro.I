import glob
import os
import socket
import subprocess
import time
from datetime import datetime

import netifaces
import psutil

from helper.Audio import Audio
from helper.Constants import Constants
from helper.PageState import PageState
from helper.StartupErrorHelper import StartupErrorHelper
from helper.Strip import Strip

audio_helper = Audio()
page_helper = PageState()
c = Constants()
startup_error_helper = StartupErrorHelper()


class SystemHelper:
    strip = Strip()
    is_party = "0"

    def __init__(self):
        self.init_party_mode()
        self._update_process: subprocess.Popen | None = None

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
        self.strip.disable()
        os.system("sudo systemctl stop retroi")

    def restart_app(self):
        self.strip.disable()
        os.system("sudo systemctl restart retroi")

    def change_revision(self, revision: str):
        self._update_process = subprocess.Popen(
            ["bash", "scripts/update_project.sh", revision],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        stdout, stderr = self._update_process.communicate()
        if self._update_process.returncode != 0:
            print("Error:", stderr)

    def cancel_revision_update(self):
        if self._update_process and self._update_process.poll() is None:
            self._update_process.terminate()
            try:
                self._update_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self._update_process.kill()  # Force kill with SIGKILL

        startup_error_helper.write_startup_error("Letztes Update abgebrochen!")
        self._update_process = None

    def get_cpu_temp(self) -> str:
        line = subprocess.run(["vcgencmd", "measure_temp"], stdout=subprocess.PIPE).stdout.decode(
            "utf-8"
        )
        temp = line[5:].strip()
        return temp

    def get_curr_date(self) -> str:
        return datetime.today().strftime("%d.%m.%Y")

    def get_download_rate(self) -> float:
        old_value = psutil.net_io_counters()
        old_recv = old_value.bytes_recv

        new_value = psutil.net_io_counters()
        download_speed = (new_value.bytes_recv - old_recv) / 1024  # KB/s

        return download_speed

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

    def open_keyboard(self):
        self.close_keyboard()
        os.system("squeekboard &")

    def close_keyboard(self):
        os.system("pkill squeekboard")

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
        factor = value / 100
        brightness = int(factor * 255)

        def try_dsi_screens():
            paths = glob.glob("/sys/class/backlight/*/brightness")
            for path in paths:
                subprocess.run(["sudo", "tee", path], input=str(brightness).encode(), check=True)

        def try_hdmi_screens():
            os.system(f"xrandr --output HDMI-0 --brightness {factor}")
            os.system(f"xrandr --output HDMI-1 --brightness {factor}")

        try_dsi_screens()
        try_hdmi_screens()

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
