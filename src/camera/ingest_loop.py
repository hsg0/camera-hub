import os
import time
import cv2

from src.camera.camera_factory import create_camera
from src.config import (
    CAMERA_SOURCE_TYPE,
    CAMERA_SOURCE_VALUE,
    SNAPSHOT_DIR,
    SNAPSHOT_INTERVAL_SECONDS,
)
from src.utils.logger import log


def main() -> None:
    os.makedirs(SNAPSHOT_DIR, exist_ok=True)

    camera = create_camera(CAMERA_SOURCE_TYPE, CAMERA_SOURCE_VALUE)

    log(f"Connecting to camera source: type={CAMERA_SOURCE_TYPE}, value={CAMERA_SOURCE_VALUE}")
    if not camera.connect():
        log("ERROR: Failed to connect to camera source.")
        raise SystemExit(1)

    log("Camera connected successfully.")
    last_snapshot_time = 0

    try:
        while True:
            ret, frame = camera.read_frame()
            if not ret or frame is None:
                log("WARNING: Failed to read frame.")
                time.sleep(1)
                continue

            now = time.time()

            if now - last_snapshot_time >= SNAPSHOT_INTERVAL_SECONDS:
                filename = os.path.join(SNAPSHOT_DIR, f"ingest_loop_{int(now)}.jpg")
                cv2.imwrite(filename, frame)
                log(f"Saved snapshot to: {filename}")
                last_snapshot_time = now

            time.sleep(0.2)

    except KeyboardInterrupt:
        log("Stopping ingest loop...")

    finally:
        camera.release()
        log("Camera released.")


if __name__ == "__main__":
    main()
