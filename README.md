# Hand Gesture HCI

Webcam-based hand gesture control using MediaPipe + rule-based classification + pyautogui.
No ML training. No GUI framework. ~300 lines of code.

## Run

```bash
pip install -r requirements.txt
python main.py
```

Optional flags:
```
--camera N         camera device index (default 0)
--width  / --height   capture resolution (default 1280x720)
```

## Gestures

| Gesture     | Action          |
|-------------|-----------------|
| Fist        | Pause / play    |
| Palm        | Scroll down     |
| Thumb up    | Volume up       |
| Thumb down  | Volume down     |
| Point       | Move cursor     |
| Peace       | Scroll up       |
| Pinch       | Left click      |

## Pipeline

```
frame -> HandTracker (MediaPipe, 21 landmarks)
      -> classify()    (geometric rules)
      -> GestureMapper (debounce + continuous/one-shot)
      -> execute()     (pyautogui / amixer)
```

## Project layout

```
main.py
requirements.txt
app/
  webcam_app.py        capture loop + HUD
src/
  hand_tracking.py     MediaPipe wrapper
  gesture_classifier.py  geometric rules
  gesture_mapper.py    gesture -> action + debounce
  system_control.py    OS event dispatch
```

## Customising

- Remap a gesture: edit `GESTURE_MAP` in `src/gesture_mapper.py`.
- Adjust debounce: `GestureMapper(debounce=...)` in `app/webcam_app.py`.
- Add a gesture rule: extend `classify()` in `src/gesture_classifier.py`,
  add it to `GESTURE_MAP`, and handle it in `system_control.py`.

## Platform notes

- macOS / Windows: `volumeup` / `volumedown` keypress.
- Linux: shells out to `amixer` (install `alsa-utils`).

## License

MIT.
