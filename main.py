"""Entry point.

Usage:
    python main.py
    python main.py --camera 1
    python main.py --width 640 --height 480
"""

import argparse

from app.webcam_app import run


def parse_args():
    p = argparse.ArgumentParser(description="Hand Gesture HCI")
    p.add_argument("--camera", type=int, default=0, help="camera device index")
    p.add_argument("--width", type=int, default=1280, help="capture width")
    p.add_argument("--height", type=int, default=720, help="capture height")
    return p.parse_args()


if __name__ == "__main__":
    args = parse_args()
    run(camera_index=args.camera, width=args.width, height=args.height)
