from arduino.app_bricks.web_ui import WebUI
from webradio import WebRadio
from arduino.app_utils import App

ui = WebUI()
radio = WebRadio()


def api_info():
    return radio.play("info")


def api_rtl():
    return radio.play("rtl")


def api_inter():
    return radio.play("inter")


def api_musique():
    return radio.play("musique")


def api_nostalgie():
    return radio.play("nostalgie")


def api_mradio():
    return radio.play("mradio")


def api_stop():
    return radio.stop()


def api_volume(value="50"):
    return radio.set_volume(value)


def api_status():
    return radio.status()


ui.expose_api("GET", "/api/info", api_info)
ui.expose_api("GET", "/api/rtl", api_rtl)
ui.expose_api("GET", "/api/inter", api_inter)
ui.expose_api("GET", "/api/musique", api_musique)
ui.expose_api("GET", "/api/nostalgie", api_nostalgie)
ui.expose_api("GET", "/api/mradio", api_mradio)
ui.expose_api("GET", "/api/stop", api_stop)
ui.expose_api("GET", "/api/volume", api_volume)
ui.expose_api("GET", "/api/status", api_status)

App.run()
