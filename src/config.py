from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DEFAULT_CAMERA_INDEX = 0
FRAME_WIDTH = 640
FRAME_HEIGHT = 480
SNAPSHOT_DIR = str(PROJECT_ROOT / "storage" / "snapshots")
