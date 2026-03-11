from src.camera.local_camera import LocalCamera
from src.camera.ip_camera import IPCamera


def create_camera(source_type: str, source_value):
    if source_type == "local":
        return LocalCamera(camera_index=int(source_value))

    if source_type == "ip":
        return IPCamera(stream_url=str(source_value))

    raise ValueError(f"Unsupported camera source type: {source_type}")
