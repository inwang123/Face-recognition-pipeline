import base64
import json
from pathlib import Path

image_path = Path("../CSE546-datasets/video_frames_100/video_frames_100/test_06.jpg")

with open(image_path, "rb") as f:
    encoded = base64.b64encode(f.read()).decode("utf-8")

mqtt_message = {
    "request_id": "demo-request-001",
    "sequence": 0,
    "filename": image_path.name,
    "encoded": encoded
}

print("1. Dataset image loaded:", image_path)
print("2. Image Base64 encoded")
print("3. MQTT-style JSON message created")
print(json.dumps({k: v if k != "encoded" else "<base64 image bytes>" for k, v in mqtt_message.items()}, indent=2))
print("4. In AWS, this message would go to Greengrass FaceDetection")
print("5. FaceDetection would crop face and send to SQS")
print("6. Lambda FaceNet classifier would return name")
