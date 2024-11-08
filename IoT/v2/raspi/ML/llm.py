# FILE: llm.py
import cv2
import torch
import pyttsx3
from picamera2 import Picamera2
import time
import numpy as np

# Initialize YOLOv5 Nano model
model = torch.hub.load('ultralytics/yolov5', 'yolov5n', pretrained=True)
model.conf = 0.5  # Confidence threshold
model.classes = None  # Detect all classes

# Initialize Camera
picam2 = Picamera2()
picam2.configure(picam2.create_still_configuration(main={"format": "RGB888", "size": (320, 240)}))
picam2.start()

# Initialize TTS Engine
tts_engine = pyttsx3.init()
voices = tts_engine.getProperty('voices')
for voice in voices:
    if 'samantha' in voice.id.lower():  # Example for macOS
        tts_engine.setProperty('voice', voice.id)
        break
tts_engine.setProperty('rate', 150)
tts_engine.setProperty('volume', 1.0)

def determine_direction(detections):
    directions = []
    for *xyxy, conf, cls in detections:
        x_center = (xyxy[0] + xyxy[2]) / 2
        if x_center < 106:  # Left third
            directions.append('right')
        elif x_center > 214:  # Right third
            directions.append('left')
        else:  # Center third
            directions.append('straight')
    if directions:
        # Prioritize the most common direction
        direction = max(set(directions), key=directions.count)
        return direction
    return 'straight'

def text_to_speech(direction):
    instruction = f"Please turn {direction}."
    tts_engine.say(instruction)
    tts_engine.runAndWait()

def main():
    processing_interval = 2  # seconds
    last_processing_time = time.time()

    while True:
        current_time = time.time()
        if current_time - last_processing_time >= processing_interval:
            frame = picam2.capture_array()
            results = model(frame)
            detections = results.xyxy[0].numpy()  # [x1, y1, x2, y2, conf, cls]

            direction = determine_direction(detections)
            print(f"Safe direction: {direction}")
            text_to_speech(direction)

            last_processing_time = current_time

        time.sleep(0.1)  # Prevent 100% CPU usage

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Terminating...")
    finally:
        picam2.stop()