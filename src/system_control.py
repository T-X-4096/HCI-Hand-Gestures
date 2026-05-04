"""Translate action names into OS-level events via pyautogui."""

import platform
import subprocess
from typing import List, Optional, Tuple

import pyautogui

pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.0

_OS = platform.system()              # "Windows" | "Darwin" | "Linux"
_SCREEN_W, _SCREEN_H = pyautogui.size()
_DEAD_ZONE = 0.10                    # mouse-mapping margin

Landmark = Tuple[float, float, float]


def _volume(direction: str) -> None:
    """direction: 'up' or 'down'."""
    if _OS == "Linux":
        sign = "+" if direction == "up" else "-"
        subprocess.Popen(
            ["amixer", "-q", "sset", "Master", f"5%{sign}"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    else:
        pyautogui.press(f"volume{direction}")


def _move_mouse(landmarks: Optional[List[Landmark]]) -> None:
    if landmarks is None:
        return
    # Mirror x because the displayed frame is mirrored.
    fx = 1.0 - landmarks[8][0]
    fy = landmarks[8][1]
    span = 1.0 - 2 * _DEAD_ZONE
    fx = min(max(fx, _DEAD_ZONE), 1.0 - _DEAD_ZONE)
    fy = min(max(fy, _DEAD_ZONE), 1.0 - _DEAD_ZONE)
    sx = int((fx - _DEAD_ZONE) / span * _SCREEN_W)
    sy = int((fy - _DEAD_ZONE) / span * _SCREEN_H)
    pyautogui.moveTo(sx, sy)


_ACTIONS = {
    "PAUSE_PLAY":  lambda lm: pyautogui.press("space"),
    "VOLUME_UP":   lambda lm: _volume("up"),
    "VOLUME_DOWN": lambda lm: _volume("down"),
    "MOVE_MOUSE":  _move_mouse,
    "SCROLL_UP":   lambda lm: pyautogui.scroll(3),
    "SCROLL_DOWN": lambda lm: pyautogui.scroll(-3),
    "CLICK":       lambda lm: pyautogui.click(),
}


def execute(action: str, landmarks: Optional[List[Landmark]] = None) -> None:
    fn = _ACTIONS.get(action)
    if fn is not None:
        fn(landmarks)
