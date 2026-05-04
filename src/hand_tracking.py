"""Wrap MediaPipe Hands. Returns 21 normalised landmarks per frame."""

from typing import Optional

import cv2
import mediapipe as mp
import numpy as np


class HandTracker:
    """Detects one hand and returns landmarks in [0,1] coords."""

    def __init__(
        self,
        max_hands: int = 1,
        detection_confidence: float = 0.7,
        tracking_confidence: float = 0.6,
    ):
        self._mp_hands = mp.solutions.hands
        self._mp_draw = mp.solutions.drawing_utils
        self._mp_styles = mp.solutions.drawing_styles
        self.hands = self._mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=max_hands,
            min_detection_confidence=detection_confidence,
            min_tracking_confidence=tracking_confidence,
        )

    def get_landmarks(self, frame: np.ndarray):
        """Process a BGR frame. Returns (landmarks, hand_label, annotated_frame)."""
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        rgb.flags.writeable = False
        results = self.hands.process(rgb)

        if not results.multi_hand_landmarks:
            return None, None, frame

        hand_lm = results.multi_hand_landmarks[0]
        handedness = results.multi_handedness[0].classification[0].label

        self._mp_draw.draw_landmarks(
            frame,
            hand_lm,
            self._mp_hands.HAND_CONNECTIONS,
            self._mp_styles.get_default_hand_landmarks_style(),
            self._mp_styles.get_default_hand_connections_style(),
        )

        landmarks = [(lm.x, lm.y, lm.z) for lm in hand_lm.landmark]
        return landmarks, handedness, frame

    def release(self):
        self.hands.close()
