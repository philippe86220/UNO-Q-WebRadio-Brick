import json
import time
from urllib.request import urlopen
from urllib.error import URLError, HTTPError


class WebRadio:
    def __init__(self, host="http://172.17.0.1:9000"):
        self.host = host
        self.station = "none"
        self.volume = 50
        self.running = False

    def _get_json(self, path):
        try:
            with urlopen(self.host + path, timeout=3) as response:
                return json.loads(response.read().decode("utf-8"))
        except HTTPError as e:
            return {"ok": False, "error": "HTTP error", "code": e.code}
        except URLError as e:
            return {"ok": False, "error": "URL error", "details": str(e)}
        except Exception as e:
            return {"ok": False, "error": "Unexpected error", "details": str(e)}

    def play(self, station):
        result = self._get_json("/" + station)

        if result.get("ok"):
            self.station = station
            self.running = True

        return {
            "ok": result.get("ok", False),
            "station": self.station,
            "running": self.running,
            "raw": result
        }

    def stop(self):
        result = self._get_json("/stop")

        if result.get("ok"):
            self.running = False

        return {
            "ok": result.get("ok", False),
            "station": self.station,
            "running": self.running,
            "raw": result
        }

    def set_volume(self, value):
        try:
            value = int(value)
        except Exception:
            value = 50

        value = max(0, min(100, value))

        result = self._get_json("/volume?value=" + str(value))

        if result.get("ok"):
            self.volume = value

        return {
            "ok": result.get("ok", False),
            "volume": self.volume,
            "raw": result
        }

    def status(self):
        return {
            "ok": True,
            "station": self.station,
            "volume": self.volume,
            "running": self.running
        }

    def run(self):
        print("[WebRadio brick] App running")
        while True:
            time.sleep(1)
