import os
import re
import subprocess


class WifiHelper:
    def is_enabled(self):
        result = subprocess.run(["rfkill", "list", "wifi"], capture_output=True, text=True)

        return "Soft blocked: no" in result.stdout

    def toggle_wifi(self):
        if self.is_enabled():
            self.disable_wifi()
        else:
            self.enable_wifi()

    def enable_wifi(self):
        subprocess.run(["sudo", "nmcli", "radio", "wifi", "on"])

    def disable_wifi(self):
        subprocess.run(["sudo", "nmcli", "radio", "wifi", "off"])

    def is_connected(self):
        ip = (
            subprocess.run(["hostname", "-I"], stdout=subprocess.PIPE)
            .stdout.decode("utf-8")
            .strip()
        )
        return ip != ""

    def get_networks(self):
        networks = os.popen("sudo iwlist wlan0 scanning | grep ESSID").read()
        networkslist = re.findall(r'"(.+?)"', networks)
        return list(dict.fromkeys(networkslist))

    def connect_to_wifi(self, ssid, password):
        if password == "":
            command = ["sudo", "nmcli", "d", "wifi", "connect", ssid]
        else:
            command = ["sudo", "nmcli", "d", "wifi", "connect", ssid, "password", password]

        subprocess.run(command, stdout=subprocess.PIPE).stdout.decode("utf-8").strip()
