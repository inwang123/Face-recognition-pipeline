import base64
import json
from pathlib import Path

image_path = Path("../datasets/video_frames_100/video_frames_100/test_06.jpg")

with open(image_path, "rb") as f:
    encoded = base64.b64encode(f.read()).decode("utf-8")

mqtt_message = {
    "request_id": "demo-request-001",
    "sequence": 0,
    "filename": image_path.name,
    "encoded": encoded
}

