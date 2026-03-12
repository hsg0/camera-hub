import os
import time
import cv2

from src.camera.camera_factory import create_camera
from src.config import CAMERA_SOURCE_TYPE, CAMERA_SOURCE_VALUE, SNAPSHOT_DIR
from src.utils.logger import log

MOTION_THRESHOLD = 290         # min changed pixels to consider motion (640x480 ~ 0.16%)
MIN_CONTOUR_AREA = 300         # ignore contours smaller than this (filters sensor noise)
MOTION_COOLDOWN_SECONDS = 5


def main() -> None:
    os.makedirs(SNAPSHOT_DIR, exist_ok=True)

    camera = create_camera(CAMERA_SOURCE_TYPE, CAMERA_SOURCE_VALUE)

    log(f"Connecting to camera source: type={CAMERA_SOURCE_TYPE}, value={CAMERA_SOURCE_VALUE}")
    if not camera.connect():
        log("ERROR: Failed to connect to camera source.")
        raise SystemExit(1)

    log("Camera connected successfully.")

    ret, prev_frame = camera.read_frame()
    if not ret or prev_frame is None:
        log("ERROR: Failed to read initial frame.")
        camera.release()
        raise SystemExit(1)

    prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
    prev_gray = cv2.GaussianBlur(prev_gray, (21, 21), 0)

    log("Initial frame captured. Motion detection is now active.")

    last_motion_save = 0

    try:
        while True:
            ret, frame = camera.read_frame()
            if not ret or frame is None:
                log("WARNING: Failed to read frame.")
                time.sleep(1)
                continue

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray = cv2.GaussianBlur(gray, (21, 21), 0)

            frame_delta = cv2.absdiff(prev_gray, gray)
            thresh = cv2.threshold(frame_delta, 25, 255, cv2.THRESH_BINARY)[1]
            thresh = cv2.dilate(thresh, None, iterations=2)

            contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            significant_contours = [c for c in contours if cv2.contourArea(c) >= MIN_CONTOUR_AREA]
            motion_score = thresh.sum() / 255

            now = time.time()
            if (motion_score > MOTION_THRESHOLD
                    and significant_contours
                    and (now - last_motion_save) >= MOTION_COOLDOWN_SECONDS):
                filename = os.path.join(SNAPSHOT_DIR, f"motion_{int(now)}.jpg")
                cv2.imwrite(filename, frame)
                log(f"MOTION DETECTED (score={int(motion_score)}, contours={len(significant_contours)}) -> {filename}")
                last_motion_save = now

            prev_gray = gray
            time.sleep(0.2)

    except KeyboardInterrupt:
        log("Stopping motion loop...")

    finally:
        camera.release()
        log("Camera released.")


if __name__ == "__main__":
    main()
