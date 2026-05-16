import base64
import json
import os
import tempfile
from io import BytesIO

import boto3
from PIL import Image
from facenet_pytorch import MTCNN


ASU_ID = "YOUR_ASU_ID"
REQUEST_QUEUE_URL = "YOUR_REQ_QUEUE_URL"

sqs = boto3.client("sqs", region_name="us-east-1")
mtcnn = MTCNN(image_size=160, margin=0)


def process_message(message: dict):
    request_id = message["request_id"]
    filename = message["filename"]
    encoded = message["encoded"]

    image_bytes = base64.b64decode(encoded)
    image = Image.open(BytesIO(image_bytes)).convert("RGB")

    face = mtcnn(image)

    if face is None:
        print(f"No face detected for {filename}")
        return

    with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tmp:
        face_image = Image.fromarray(
            face.permute(1, 2, 0).byte().numpy()
        )
        face_image.save(tmp.name)

        with open(tmp.name, "rb") as f:
            cropped_encoded = base64.b64encode(f.read()).decode("utf-8")

    sqs.send_message(
        QueueUrl=REQUEST_QUEUE_URL,
        MessageBody=json.dumps({
            "request_id": request_id,
            "filename": filename,
            "encoded": cropped_encoded
        })
    )

    print(f"Sent detected face for {filename} to SQS")


if __name__ == "__main__":
    print("This is the Greengrass FaceDetection component.")
    print("In the real project, this subscribed to MQTT topic:")
    print(f"clients/{ASU_ID}-IoTThing")
