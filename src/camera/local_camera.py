import cv2
from camera.base_camera import BaseCamera
from config import DEFAULT_CAMERA_INDEX, FRAME_WIDTH, FRAME_HEIGHT


class LocalCamera(BaseCamera):
    def __init__(self, camera_index: int = DEFAULT_CAMERA_INDEX):
        self.camera_index = camera_index
        self.cap = None

    def connect(self) -> bool:
        self.cap = cv2.VideoCapture(self.camera_index)
        if not self.cap or not self.cap.isOpened():
            return False

        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)
        return True

    def read_frame(self):
        if not self.cap:
            return False, None
        return self.cap.read()

    def release(self) -> None:
        if self.cap:
            self.cap.release()

    def is_open(self) -> bool:
        return bool(self.cap and self.cap.isOpened())
