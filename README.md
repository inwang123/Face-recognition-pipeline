# AWS IoT Greengrass Face Recognition Pipeline

Distributed edge/cloud face-recognition pipeline using:

- AWS IoT Greengrass
- MQTT
- Amazon SQS
- AWS Lambda
- FaceNet
- MTCNN
- PyTorch

## Architecture

Dataset Image
→ MQTT Message
→ Greengrass FaceDetection Component
→ SQS Request Queue
→ Lambda Face Recognition
→ SQS Response Queue

## Components

### face-detection/fd_component.py
Edge component responsible for:
- MQTT subscription
- Base64 image decoding
- MTCNN face detection
- forwarding cropped faces to SQS

### face-recognition/fr_lambda.py
Lambda recognition component responsible for:
- SQS event handling
- FaceNet inference
- returning classification results

### local_demo.py
Local reconstruction/demo of the MQTT payload generation flow.

## Notes

This project reconstructs the architecture of a cloud computing course project.

Pretrained FaceNet and MTCNN models were integrated into a distributed AWS pipeline for edge/cloud face recognition.
