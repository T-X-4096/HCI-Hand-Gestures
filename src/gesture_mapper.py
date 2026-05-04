"""Map gesture names to action names. Handle debouncing."""

import time
from typing import Optional

# Gesture → action.
# FIST handles pause/play; PALM does scroll-down (avoids redundant space-press).
GESTURE_MAP = {
    "FIST":       "PAUSE_PLAY",
    "PALM":       "SCROLL_DOWN",
    "THUMB_UP":   "VOLUME_UP",
    "THUMB_DOWN": "VOLUME_DOWN",
    "POINT":      "MOVE_MOUSE",
    "PEACE":      "SCROLL_UP",
    "PINCH":      "CLICK",
}

# Continuous = fires every interval while held.
# One-shot = fires once per gesture-change, then waits for debounce.
CONTINUOUS = {"MOVE_MOUSE", "SCROLL_UP", "SCROLL_DOWN", "VOLUME_UP", "VOLUME_DOWN"}
ONE_SHOT = {"PAUSE_PLAY", "CLICK"}


class GestureMapper:
    def __init__(self, debounce: float = 0.55, continuous_interval: float = 0.05):
        self._debounce = debounce
        self._cont_iv = continuous_interval
        self._last_gesture: Optional[str] = None
        self._last_fire = 0.0

    def get_action(self, gesture: Optional[str]) -> Optional[str]:
        action = GESTURE_MAP.get(gesture) if gesture else None
        if action is None:
            self._last_gesture = None
            return None

        now = time.monotonic()
        if gesture != self._last_gesture:
            self._last_gesture = gesture
            self._last_fire = 0.0  # fire immediately on change

        elapsed = now - self._last_fire
        interval = self._cont_iv if action in CONTINUOUS else self._debounce
        if elapsed >= interval:
            self._last_fire = now
            return action
        return None
