![Arduino App Lab](https://img.shields.io/badge/Arduino%20App%20Lab-0.7.0-blue)
![Platform](https://img.shields.io/badge/macOS-26.3.1-lightgrey)
![Target](https://img.shields.io/badge/Board-UNO%20Q-green)
![Python](https://img.shields.io/badge/Python-3.x-yellow)
![Audio](https://img.shields.io/badge/Audio-ALSA%20%2F%20mpg123-red)
![Container](https://img.shields.io/badge/Container-Docker-orange)

# UNO-Q-WebRadio-Brick

## Introduction

This project explores advanced custom brick capabilities in Arduino App Lab 0.7.0 on the UNO Q platform.

It demonstrates how a custom brick can encapsulate:

- radio application logic
- a containerized Linux audio service
- internal HTTP communication
- ALSA audio playback
- MP3 streaming management

while remaining easily usable from a WebUI-based App Lab application.

The project implements a fully functional Web Radio architecture using:

- App Lab Python
- a WebUI frontend
- a custom local brick
- a Docker container
- mpg123
- ALSA
- and a USB audio device

---

## Main Goal

The purpose of this project is to explore how custom bricks can be used to build modular and reusable application architectures on UNO Q.

The project also demonstrates that Linux audio devices can be exposed inside custom brick containers using:

```yaml
devices:
  - /dev/snd
```

This allows direct ALSA audio playback from inside the brick service container.

---

## Global Architecture

Final architecture:

```text
WebUI HTML
    ↓
main.py
    ↓
WebRadio Brick API
    ↓
radio_service.py
    ↓
mpg123
    ↓
ALSA (/dev/snd)
    ↓
USB Audio Device
```

---

## Project Overview

The application is composed of:

### WebUI

Provides:

- radio selection buttons
- volume control
- playback status

---

### main.py

Exposes HTTP APIs to the WebUI using:

```python
ui.expose_api()
```

Example:

```python
ui.expose_api("GET", "/api/info", api_info)
```

---

### Custom Brick

The `WebRadio` brick encapsulates:

- station playback
- volume management
- status handling
- communication with the container service

Example:

```python
from webradio import WebRadio

radio = WebRadio()

radio.play("info")
radio.set_volume(50)
radio.stop()
```

---

### Containerized Audio Service

The brick includes its own container service defined in:

```text
brick_compose.yaml
```

The service:

- installs mpg123
- installs ALSA utilities
- exposes `/dev/snd`
- launches `radio_service.py`

---

## brick_compose.yaml

```yaml
services:
  player:
    image: debian:bookworm-slim
    user: root

    devices:
      - /dev/snd

    volumes:
      - .:/webradio

    command: >
      sh -c "
      apt update &&
      apt install -y python3 mpg123 alsa-utils procps curl ca-certificates &&
      exec python3 /webradio/radio_service.py
      "
```

---

## Audio Backend

Audio playback is performed using:

```bash
mpg123
```

with ALSA output:

```bash
-o alsa
-a hw:0,0
```

---

## Supported Radio Stations

Current examples:

- France Info
- RTL
- France Inter
- France Musique
- Nostalgie
- M Radio

Stations are defined inside:

```python
RADIOS = {
    ...
}
```

---

## HTTP API

The internal container service exposes endpoints such as:

```text
/info
/rtl
/inter
/musique
/nostalgie
/mradio
/stop
/status
/volume?value=50
```

---

## Example WebUI Call

```javascript
fetch("/api/info")
```

---

## What This Project Demonstrates

This repository demonstrates:

✔ custom App Lab bricks

✔ containerized services

✔ ALSA access from containers

✔ MP3 audio streaming

✔ reusable Python APIs

✔ modular architecture

✔ WebUI integration

✔ hardware access through `brick_compose.yaml`

---

## Why This Matters

This project highlights an important capability of UNO Q and App Lab:

Custom brick containers can access Linux hardware devices when explicitly exposed through Docker compose configuration.

This opens the door to:

- audio applications
- multimedia projects
- hardware-oriented Linux services
- advanced hybrid MPU applications

---

## Repository Structure

```text
assets/
    index.html

bricks/
    webradio/
        README.md
        __init__.py
        brick_config.yaml
        brick_compose.yaml
        radio_service.py

python/
    main.py

LICENSE
README.md
app.yaml
```

---

## First Startup Behavior

On first startup, the container dynamically installs required Debian packages such as:

- python3
- mpg123
- alsa-utils
- curl

Because of this initialization step, the radio service may take approximately 30 to 60 seconds before becoming operational on a fresh installation.

Once initialization is complete, radio playback becomes immediately available.

---

## Credits

This project was developed through experimentation and architectural exploration of the UNO Q platform.

It also benefited from technical discussions and architectural exploration with ChatGPT (OpenAI).

---

## License

MIT License
