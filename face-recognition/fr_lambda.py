__copyright__ = "Copyright 2025, VISA Lab"
__license__ = "MIT"

import base64
import json
import os
import tempfile

import boto3
import torch
from PIL import Image
from facenet_pytorch import MTCNN, InceptionResnetV1

RESPONSE_QUEUE_URL = os.environ.get("RESPONSE_QUEUE_URL", "YOUR_RESP_QUEUE_URL")

sqs = boto3.client("sqs", region_name="us-east-1")

mtcnn = MTCNN(image_size=240, margin=0, min_face_size=20)
resnet = InceptionResnetV1(pretrained="vggface2").eval()


def face_match(img_path, data_path="data.pt"):
    img = Image.open(img_path).convert("RGB")

    face, prob = mtcnn(img, return_prob=True)

    if face is None:
        return "No-Face", 0.0

    emb = resnet(face.unsqueeze(0)).detach()

    saved_data = torch.load(data_path, map_location=torch.device("cpu"))
    embedding_list = saved_data[0]
    name_list = saved_data[1]

    dist_list = []

    for emb_db in embedding_list:
        dist = torch.dist(emb, emb_db).item()
        dist_list.append(dist)

    idx_min = dist_list.index(min(dist_list))
    return name_list[idx_min], min(dist_list)


def lambda_handler(event, context):
    for record in event["Records"]:
        body = json.loads(record["body"])

        request_id = body["request_id"]
        filename = body.get("filename", "unknown.jpg")
        encoded = body["encoded"]

        image_bytes = base64.b64decode(encoded)

        with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tmp:
            tmp.write(image_bytes)
            tmp_path = tmp.name

        result, distance = face_match(tmp_path, "data.pt")

        response_payload = {
            "request_id": request_id,
            "filename": filename,
            "result": result,
        }

        sqs.send_message(
            QueueUrl=RESPONSE_QUEUE_URL, MessageBody=json.dumps(response_payload)
        )

        print(f"Processed {filename}: {result}, distance={distance}")

    return {"statusCode": 200, "body": "processed"}


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python3 fr_lambda.py <image_path>")
        sys.exit(1)

    result, distance = face_match(sys.argv[1], "data.pt")
    print(result)
