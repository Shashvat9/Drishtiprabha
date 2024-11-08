from ultralytics import YOLO
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import pyttsx3
from picamera2 import Picamera2
import numpy as np
import time

# Load YOLO model (Using YOLOv8 for demonstration purposes)
model = YOLO('yolov8n.pt') 


picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration(main={"format": "RGB888", "size": (640, 480)}))
picam2.start()


tts_engine = pyttsx3.init()


tokenizer = GPT2Tokenizer.from_pretrained("distilgpt2")
llm_model = GPT2LMHeadModel.from_pretrained("distilgpt2")


def get_navigation_guidance(captions):
    navigation_guidances = []
    for caption in captions:
        prompt = f"{caption}. hithere."
        print(prompt)
        inputs = tokenizer(prompt, return_tensors="pt")
        outputs = llm_model.generate(**inputs, max_length=50)
        guidance = tokenizer.decode(outputs[0], skip_special_tokens=True)
        navigation_guidances.append(guidance)
    return navigation_guidances


def text_to_speech(captions):
    caption_text = ' '.join(captions)
    tts_engine.setProperty('voice', 'com.apple.speech.synthesis.voice.samantha') 
    tts_engine.setProperty('rate', 200)
    tts_engine.say(caption_text)
    tts_engine.runAndWait()

while True:

    frame = picam2.capture_array()

    # Run YOLO detection on the captured frame
    results = model(frame)

    # Generate captions from detections (without displaying or bounding boxes)
    captions = []
    for result in results:
        for detection in result.boxes:
            class_name = model.names[int(detection.cls)]
            captions.append(f"Detected {class_name}")


    if captions:
        navigation_guidances = get_navigation_guidance(captions)
        combined_text = captions + navigation_guidances  
        text_to_speech(combined_text)


    time.sleep(1)  
