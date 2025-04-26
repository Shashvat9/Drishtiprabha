# Install required dependencies using the following commands:
# pip install ultralytics pyttsx3 torch torchvision transformers opencv-python

import threading
import queue
import time
import cv2
from ultralytics import YOLO
import pyttsx3
import RPi.GPIO as GPIO
import torch
import torchvision.models as models
from torchvision import transforms
from PIL import Image
from transformers import pipeline

shared_queue = queue.Queue()

GPIO_TRIGGER = 23
GPIO_ECHO = 24
GPIO.setmode(GPIO.BCM)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)


yolo_model = YOLO("yolov8n.pt")


embedding_model = models.resnet18(pretrained=True)
embedding_model.eval()


preprocess = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])


llm_generator = pipeline("text-generation", model="gpt2")


tts_engine = pyttsx3.init()
tts_engine.setProperty('rate', 150)
tts_engine.setProperty('volume', 1.0)


def measure_distance():
    GPIO.output(GPIO_TRIGGER, True)
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)

    start_time = time.time()
    stop_time = time.time()

    while GPIO.input(GPIO_ECHO) == 0:
        start_time = time.time()

    while GPIO.input(GPIO_ECHO) == 1:
        stop_time = time.time()

    time_elapsed = stop_time - start_time
    distance = (time_elapsed * 34300) / 2
    return distance


def get_embedding(image):
    image = preprocess(image).unsqueeze(0)
    with torch.no_grad():
        embedding = embedding_model(image)
    return embedding


def object_detection():
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        results = yolo_model(frame)
        detected_objects = results[0].boxes.data

 
        pil_image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        embedding = get_embedding(pil_image)

        shared_queue.put(("objects", (detected_objects, embedding)))

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


def distance_sensing():
    while True:
        distance = measure_distance()
        shared_queue.put(("distance", distance))
        time.sleep(1)


def llm_and_tts():
    last_scene = None

    while True:
        if not shared_queue.empty():
            data_type, data = shared_queue.get()

            if data_type == "objects":
                detected_objects, embedding = data
                prompt = f"The scene contains objects: {detected_objects}. Provide navigation instructions."
            elif data_type == "distance":
                distance = data
                prompt = f"Distance to nearest object: {distance} cm. Provide navigation instructions."


            instructions = llm_generator(prompt, max_length=50, num_return_sequences=1)[0]['generated_text']


            if instructions != last_scene:
                tts_engine.say(instructions)
                tts_engine.runAndWait()
                last_scene = instructions

        time.sleep(0.1)


if __name__ == "__main__":
    thread1 = threading.Thread(target=object_detection)
    thread2 = threading.Thread(target=distance_sensing)
    thread3 = threading.Thread(target=llm_and_tts)

    thread1.start()
    thread2.start()
    thread3.start()

    thread1.join()
    thread2.join()
    thread3.join()