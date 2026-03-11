import os
import time
import cv2

from src.camera.local_camera import LocalCamera
from src.config import SNAPSHOT_DIR
from src.utils.logger import log


def main() -> None:
    os.makedirs(SNAPSHOT_DIR, exist_ok=True)

    camera = LocalCamera()

    log("Connecting to local camera...")
    if not camera.connect():
        log("ERROR: Failed to connect to local camera.")
        raise SystemExit(1)

    log("Camera connected successfully.")

    ret, frame = camera.read_frame()
    if not ret or frame is None:
        log("ERROR: Failed to read frame.")
        camera.release()
        raise SystemExit(1)

    filename = os.path.join(SNAPSHOT_DIR, f"ingest_test_{int(time.time())}.jpg")
    cv2.imwrite(filename, frame)
    log(f"Saved snapshot to: {filename}")

    camera.release()
    log("Camera released.")


if __name__ == "__main__":
    main()
