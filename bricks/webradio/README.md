# WebRadio Brick

## Overview

This custom App Lab brick provides a simple API
to control a host-side Linux web radio service.

The brick encapsulates:
- station selection
- volume control
- status handling
- HTTP communication

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

---

### set_volume(value)

Set volume from 0 to 100.

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

### Backend Requirement

This brick requires a Linux host-side service
providing HTTP endpoints such as:

```
/info
/rtl
/stop
/volume?value=50
```
Default host:

```
http://172.17.0.1:9000
```
### Notes
This brick runs inside the App Lab container. 
Direct ALSA access is not available inside App Lab service containers,
therefore audio playback is delegated to a Linux host-side service.
