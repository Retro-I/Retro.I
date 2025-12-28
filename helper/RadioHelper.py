import re
import struct

import requests
from requests import Response

try:
    import urllib2
except ImportError:
    import urllib.request as urllib2


class RadioHelper:
    def get_song_info(self, url) -> str:
        try:
            request = urllib2.Request(url, headers={"Icy-MetaData": 1})
            encoding = "utf-8"
            response = urllib2.urlopen(request)
            metaint = int(response.headers["icy-metaint"])
            for _ in range(10):
                response.read(metaint)
                metadata_length = struct.unpack("B", response.read(1))[0] * 16
                metadata = response.read(metadata_length).rstrip(b"\0")
                m = re.search(rb"StreamTitle='([^']*)';", metadata)
                if m:
                    title = m.group(1)
                    if title:
                        return title.decode(encoding, errors="replace")
            else:
                return ""
        except Exception:
            return ""

    def get_stations_by_name(self, name: str) -> list:
        def _call(api_prefix: str = "de1") -> Response:
            url = (
                f"https://{api_prefix}.api.radio-browser.info/json/stations/byname/{name}"
                "?order=votes&reverse=true"
            )
            return requests.get(url)

        response = _call()

        if response.status_code != 200:
            response = _call("de2")
            response.raise_for_status()

        stations = [
            {
                "name": entry.get("name", ""),
                "src": entry.get("url", ""),
                "logo": entry.get("favicon", ""),
                "color": "#46A94B",
            }
            for entry in response.json()
        ]

        return stations
