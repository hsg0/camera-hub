import cv2
from src.camera.base_camera import BaseCamera


class IPCamera(BaseCamera):
    def __init__(self, stream_url: str):
        self.stream_url = stream_url
        self.cap = None

    def connect(self) -> bool:
        self.cap = cv2.VideoCapture(self.stream_url)
        if not self.cap or not self.cap.isOpened():
            return False
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
