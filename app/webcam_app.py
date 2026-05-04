"""Main application loop: capture frame, detect gesture, fire action, render HUD."""

import time

import cv2

from src.gesture_classifier import classify
from src.gesture_mapper import GestureMapper
from src.hand_tracking import HandTracker
from src.system_control import execute

# Minimal palette (BGR).
_BG = (20, 20, 20)
_FG = (235, 235, 235)
_ACCENT = (0, 230, 118)
_MUTED = (130, 130, 130)

_GESTURE_HINTS = {
    "FIST":       "FIST  -  pause / play",
    "PALM":       "PALM  -  scroll down",
    "THUMB_UP":   "THUMB UP  -  volume +",
    "THUMB_DOWN": "THUMB DOWN  -  volume -",
    "POINT":      "POINT  -  move cursor",
    "PEACE":      "PEACE  -  scroll up",
    "PINCH":      "PINCH  -  left click",
}


def _draw_hud(frame, gesture, action, fps):
    """Render a compact bottom bar and a top status line."""
    h, w = frame.shape[:2]
    bar_h = 64

    overlay = frame.copy()
    cv2.rectangle(overlay, (0, h - bar_h), (w, h), _BG, -1)
    cv2.addWeighted(overlay, 0.65, frame, 0.35, 0, frame)

    g_text = _GESTURE_HINTS.get(gesture, "no gesture")
    g_color = _ACCENT if gesture else _MUTED
    a_text = action if action else "-"

    cv2.putText(frame, g_text, (16, h - 36),
                cv2.FONT_HERSHEY_SIMPLEX, 0.62, g_color, 2)
    cv2.putText(frame, f"action: {a_text}", (16, h - 12),
                cv2.FONT_HERSHEY_SIMPLEX, 0.55, _FG, 1)
    cv2.putText(frame, f"{fps:4.0f} fps", (w - 110, 28),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, _MUTED, 1)
    cv2.putText(frame, "Hand Gesture HCI   |   esc to quit", (16, 28),
                cv2.FONT_HERSHEY_SIMPLEX, 0.55, _FG, 1)
    return frame


def run(camera_index: int = 0, width: int = 1280, height: int = 720) -> None:
    cap = cv2.VideoCapture(camera_index)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
    cap.set(cv2.CAP_PROP_FPS, 30)

    if not cap.isOpened():
        print(f"[error] cannot open camera {camera_index}")
        return

    tracker = HandTracker(detection_confidence=0.75, tracking_confidence=0.65)
    mapper = GestureMapper(debounce=0.55, continuous_interval=0.04)

    print("[info] running. press esc or q to quit.")
    prev = time.monotonic()

    try:
        while True:
            ok, frame = cap.read()
            if not ok:
                continue
            frame = cv2.flip(frame, 1)

            landmarks, hand_label, frame = tracker.get_landmarks(frame)
            gesture = classify(landmarks, hand_label or "Right")
            action = mapper.get_action(gesture)
            if action:
                execute(action, landmarks)

            now = time.monotonic()
            fps = 1.0 / max(now - prev, 1e-9)
            prev = now

            frame = _draw_hud(frame, gesture, action, fps)
            cv2.imshow("Hand Gesture HCI", frame)

            key = cv2.waitKey(1) & 0xFF
            if key in (27, ord("q")):
                break
    finally:
        cap.release()
        tracker.release()
        cv2.destroyAllWindows()
        print("[info] session ended.")
