"""Rule-based gesture classifier. No ML.

Gestures: FIST, PALM, THUMB_UP, THUMB_DOWN, POINT, PEACE, PINCH.
"""

import math
from typing import List, Optional, Tuple

Landmark = Tuple[float, float, float]

# MediaPipe finger (tip, pip) pairs for index/middle/ring/pinky.
_FINGERS = [(8, 6), (12, 10), (16, 14), (20, 18)]


def _dist(a: Landmark, b: Landmark) -> float:
    return math.hypot(a[0] - b[0], a[1] - b[1])


def _fingers_up(landmarks: List[Landmark]) -> List[bool]:
    """Returns [index, middle, ring, pinky] extension flags."""
    return [landmarks[t][1] < landmarks[p][1] for t, p in _FINGERS]


def _thumb_extended(landmarks: List[Landmark], hand_label: str) -> bool:
    tip, ip, mcp = landmarks[4], landmarks[3], landmarks[2]
    if hand_label == "Right":
        return tip[0] < ip[0] < mcp[0]
    return tip[0] > ip[0] > mcp[0]


def classify(
    landmarks: Optional[List[Landmark]], hand_label: str = "Right"
) -> Optional[str]:
    """Classify 21 landmarks into a gesture name, or None."""
    if landmarks is None or len(landmarks) != 21:
        return None

    index_up, middle_up, ring_up, pinky_up = _fingers_up(landmarks)
    thumb_out = _thumb_extended(landmarks, hand_label)
    wrist_y, thumb_y = landmarks[0][1], landmarks[4][1]
    pinch_dist = _dist(landmarks[4], landmarks[8])

    all_curled = not any((index_up, middle_up, ring_up, pinky_up))

    # PINCH requires index extended (distinguishes from a closed fist).
    if pinch_dist < 0.06 and index_up:
        return "PINCH"

    if all_curled:
        if thumb_out and thumb_y < wrist_y - 0.10:
            return "THUMB_UP"
        if thumb_out and thumb_y > wrist_y + 0.10:
            return "THUMB_DOWN"
        return "FIST"

    if index_up and not middle_up and not ring_up and not pinky_up:
        return "POINT"

    if index_up and middle_up and not ring_up and not pinky_up:
        return "PEACE"

    if all((index_up, middle_up, ring_up, pinky_up)):
        return "PALM"

    return None
