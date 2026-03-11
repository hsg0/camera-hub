class BaseCamera:
    def connect(self) -> bool:
        raise NotImplementedError

    def read_frame(self):
        raise NotImplementedError

    def release(self) -> None:
        raise NotImplementedError

    def is_open(self) -> bool:
        raise NotImplementedError
