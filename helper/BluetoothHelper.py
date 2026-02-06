import os
import re
import subprocess

from helper.PageState import PageState
from helper.SystemHelper import SystemHelper

system_helper = SystemHelper()


class BluetoothHelper:
    discovery_on = False

    def on_startup(self):
        self.bluetooth_discovery_off()
        self.turn_off()

    def is_discovery_on(self):
        return self.discovery_on

    def toggle_bluetooth_discovery(self):
        if self.discovery_on:
            self.bluetooth_discovery_off()
        else:
            self.bluetooth_discovery_on()

        PageState.page.update()
        return self.discovery_on

    def turn_on(self):
        os.system("rfkill unblock 0")

    def turn_off(self):
        subprocess.run(["rfkill", "block", "0"], stdout=subprocess.DEVNULL)

    def is_bluetooth_on(self):
        status = subprocess.run(
            ["hciconfig"], stdout=subprocess.PIPE
        ).stdout.decode("utf-8")
        return "RUNNING" in status

    def bluetooth_discovery_on(self):
        os.system("bluetoothctl discoverable on")
        self.discovery_on = True

    def bluetooth_discovery_off(self):
        os.system("bluetoothctl discoverable off")
        self.discovery_on = False

    def get_bluetooth_display_name(self) -> str:
        result = subprocess.run(
            'bluetoothctl show | grep "Alias:" | cut -d ":" -f2-',
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True,
        )
        return result.stdout.strip()

    def change_bluetooth_display_name(self, name):
        self.turn_off()
        os.system(f'bluetoothctl system-alias "{name}"')
        self.turn_on()

    def connect(self, mac_address):
        subprocess.run(["bluetoothctl", "connect", mac_address])
        print("Device connected")

    def disconnect(self, address=None):
        if address is None:
            address = self.get_connected_device_mac()

        subprocess.run(["bluetoothctl", "disconnect", address])
        print("Device disconnected")

    def get_paired_devices(self) -> list:
        output = subprocess.check_output(
            ["bluetoothctl", "devices", "Paired"], text=True
        )

        # Each line typically looks like: "Device XX:XX:XX:XX:XX:XX Device_Name"
        devices = {}
        for line in output.strip().split("\n"):
            match = re.match(r"Device ([0-9A-F:]+) (.+)", line)
            if match:
                mac_address, name = match.groups()
                devices[mac_address] = {
                    "name": name,
                    "mac_address": mac_address,
                }

        return list(devices.values())

    def remove_device(self, address):
        subprocess.run(["bluetoothctl", "remove", address])

    def get_connected_device(self):
        return subprocess.run(
            ["bluetoothctl", "devices", "Connected"], stdout=subprocess.PIPE
        ).stdout.decode("utf-8")

    def get_connected_device_name(self):
        result = self.get_connected_device()
        return result[25:].strip()

    def is_connected(self):
        return self.get_connected_device_name() != ""

    def get_connected_device_mac(self):
        result = self.get_connected_device()
        return result[7:24]

    def is_device_connected(self):
        result = self.get_connected_device()
        return result is not None
