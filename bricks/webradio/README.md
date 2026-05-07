# WebRadio Brick

## Overview

`WebRadio` is a custom App Lab brick for UNO Q.

It provides a simple Python API to control a containerized Linux audio service.

The brick encapsulates:

- radio playback
- volume control
- playback status
- HTTP communication
- ALSA audio output

---

## Architecture

```text
Python App
    ↓
WebRadio Brick
    ↓
radio_service.py
    ↓
mpg123
    ↓
ALSA (/dev/snd)
```

---

## Features

The brick provides:

- `play(station)`
- `stop()`
- `set_volume(value)`
- `status()`

---

## Usage

```python
from webradio import WebRadio

radio = WebRadio()

radio.play("info")
radio.set_volume(50)
radio.stop()
```

---

## Methods

### play(station)

Start a radio stream.

Example:

```python
radio.play("rtl")
```

---

### stop()

Stop playback.

Example:

```python
radio.stop()
```

---

### set_volume(value)

Set playback volume from 0 to 100.

Example:

```python
radio.set_volume(75)
```

---

### status()

Return current internal state.

Example returned dictionary:

```python
{
    "ok": True,
    "station": "info",
    "volume": 50,
    "running": True
}
```

---

## Internal Audio Service

The brick includes a containerized audio backend based on:

- Python HTTP server
- mpg123
- ALSA
- USB audio output

The backend service is launched automatically using:

```text
brick_compose.yaml
```

---

## Audio Device Access

The container accesses ALSA devices using:

```yaml
devices:
  - /dev/snd
```

This allows direct audio playback from inside the brick container.

---

## Internal HTTP Endpoints

The internal service exposes endpoints such as:

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

## Notes

The brick communicates internally with the audio service using HTTP requests.

Default internal host:

```text
http://player:9000
```

---

## Example

```python
result = radio.play("nostalgie")

print(result)
```

Possible returned dictionary:

```python
{
    "ok": True,
    "station": "nostalgie",
    "running": True
}
```

---

## License

MIT License
