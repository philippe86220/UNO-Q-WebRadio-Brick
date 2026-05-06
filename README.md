# UNO-Q-Custom-Brick-Exploration-WebUI

## Overview

This project explores the capabilities and current limitations of **custom bricks in Arduino App Lab 0.7.0** on the **UNO Q platform**.

The goal is to:

* build a clean application architecture using a custom brick,
* integrate a WebUI interface,
* test containerized services via `brick_compose.yaml`,
* and evaluate access to low-level audio (ALSA / USB sound).

---

## Architecture

The final working architecture is:

```
WebUI (HTML)
    ↓
App Lab (Python)
    ↓
Custom Brick (WebRadio)
    ↓
Linux host service (systemd)
    ↓
mpg123 + ALSA + USB audio
```

### Key idea

* **App Lab container** handles UI and logic
* **Linux host** handles hardware access (audio)

---

## Custom Brick: WebRadio

A local custom brick is implemented to encapsulate all radio logic.

### Features

* `play(station)`
* `stop()`
* `set_volume(value)`
* `status()`

### Example usage

```python
from webradio import WebRadio

radio = WebRadio()

radio.play("info")
radio.set_volume(50)
radio.stop()
```

This replaces direct HTTP calls with a clean API.

---

## WebUI Interface

A simple HTML interface is used:

* station selection buttons
* volume slider
* status display

Example API call:

```javascript
fetch("/api/info")
```

---

## Backend: Linux Audio Service

Audio playback is handled by a **host-side service**:

* Python HTTP server (`radio_service.py`)
* Shell scripts using `mpg123`
* ALSA output to USB sound card

Example endpoint:

```
http://172.17.0.1:9000/info
```

---

## Containerization Test

A key part of this project was testing whether audio playback could be fully containerized using `brick_compose.yaml`.

### Test configuration

```yaml
services:
  player:
    image: debian:bookworm-slim
    command: sh -c "ls -l /dev/snd || true; sleep infinity"
```

### Test command

```bash
docker exec -it copy-of-brique-player-1 ls -l /dev/snd
```

---

## Result

```
ls: cannot access '/dev/snd': No such file or directory
```

### Interpretation

* The container runs correctly
* BUT audio devices are not exposed inside the container

---

## Conclusion

Custom bricks in App Lab:

✔ allow:

* clean architecture
* reusable logic
* API abstraction
* WebUI integration
* containerized services (non-hardware)

❌ do not currently allow:

* direct ALSA access
* USB audio output
* low-level hardware control from containers

---

## Final Design Choice

Because of this limitation, audio playback is handled outside App Lab:

```
App Lab → HTTP → Linux host → ALSA → USB audio
```

This approach is:

* robust
* reliable
* compatible with current platform constraints

---

## Why this matters

This project demonstrates:

* how to properly structure an App Lab application
* how to use custom bricks effectively
* and where the current platform boundaries are

---

## Future Improvements

Potential enhancements for App Lab:

* expose `/dev/snd` to containers
* provide official audio output API
* support USB audio devices inside bricks

---

## Repository Content

```
assets/
    index.html

python/
    main.py

bricks/
    webradio/
        __init__.py
        brick_config.yaml
        brick_compose.yaml

host/
    radio_service.py
    scripts/
```

---

## Credits

This project was developed through iterative experimentation and architectural exploration of the UNO Q platform.

---

## License

MIT License
