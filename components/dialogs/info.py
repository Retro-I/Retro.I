import flet as ft

from core.factories.helper_factories import (
    create_revision_helper,
    create_system_helper,
)


class Info(ft.ListView):
    def __init__(self):
        super().__init__()
        self.system_helper = create_system_helper()
        self.revision_helper = create_revision_helper()

        self.version_text = ft.TextSpan("")
        self.cpu_temp_text = ft.TextSpan("")
        self.download_rate_text = ft.TextSpan("")
        self.ssid_text = ft.TextSpan("")
        self.ip_text = ft.TextSpan("")
        self.hostname_text = ft.TextSpan("")
        self.subnetmask_text = ft.TextSpan("")
        self.mac_text = ft.TextSpan("")
        self.gateway_text = ft.TextSpan("")
        self.dns_pri_text = ft.TextSpan("")
        self.dns_sec_text = ft.TextSpan("")

        self.expand = True
        self.controls = [
            ft.Text("System", weight=ft.FontWeight.BOLD, size=28),
            ft.Text(
                spans=[ft.TextSpan("Version: "), self.version_text],
                size=20,
            ),
            ft.Text(
                spans=[
                    ft.TextSpan("Datum: "),
                    ft.TextSpan(self.system_helper.get_curr_date()),
                ],
                size=20,
            ),
            ft.Text(
                spans=[ft.TextSpan("CPU-Temperatur: "), self.cpu_temp_text],
                size=20,
            ),
            ft.Text(
                spans=[
                    ft.TextSpan("Downloadrate: "),
                    self.download_rate_text,
                    ft.TextSpan(" kB/s"),
                ],
                size=20,
            ),
            ft.Divider(),
            ft.Text("IP-Config", weight=ft.FontWeight.BOLD, size=28),
            ft.Text(spans=[ft.TextSpan("SSID: "), self.ssid_text], size=20),
            ft.Text(spans=[ft.TextSpan("IP-Adresse: "), self.ip_text], size=20),
            ft.Text(
                spans=[ft.TextSpan("Hostname: "), self.hostname_text],
                size=20,
            ),
            ft.Text(
                spans=[ft.TextSpan("Subnetzmaske: "), self.subnetmask_text],
                size=20,
            ),
            ft.Text(
                spans=[ft.TextSpan("MAC-Adresse: "), self.mac_text], size=20
            ),
            ft.Text(
                spans=[ft.TextSpan("Gateway: "), self.gateway_text], size=20
            ),
            ft.Text(
                spans=[ft.TextSpan("DNS Primär: "), self.dns_pri_text],
                size=20,
            ),
            ft.Text(
                spans=[ft.TextSpan("DNS Sekundär: "), self.dns_sec_text],
                size=20,
            ),
        ]

    def set_system_info(self):
        self.version_text.text = self.revision_helper.get_current_revision()
        self.cpu_temp_text.text = self.system_helper.get_cpu_temp()
        self.download_rate_text.text = round(
            self.system_helper.get_download_rate(), 2
        )
        self.update()
        self.update_ip_config()

    def update_ip_config(self):
        ip_config = self.system_helper.get_network_config()

        self.ssid_text.text = ip_config["ssid"] or ""
        self.ip_text.text = ip_config["ip"] or ""
        self.hostname_text.text = ip_config["hostname"] or ""
        self.subnetmask_text.text = ip_config["subnetmask"] or ""
        self.mac_text.text = ip_config["mac_address"] or ""
        self.gateway_text.text = ip_config["gateway"] or ""
        self.dns_pri_text.text = ip_config["dns"][0] or ""
        try:
            self.dns_sec_text.text = ip_config["dns"][1] or ""
        except IndexError:
            self.dns_sec_text.text = ""

        self.update()
