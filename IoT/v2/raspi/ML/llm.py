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
        prompt = f"System has detected {caption}. Provide a clear and concise navigation instruction to avoid this object.Left, right, or straight?"
        inputs = tokenizer(prompt, return_tensors="pt")
        outputs = llm_model.generate(
            **inputs,
            max_length=50,
            num_return_sequences=1,
            no_repeat_ngram_size=2,
            temperature=0.7,
            top_p=0.9,
            eos_token_id=tokenizer.eos_token_id
        )
        guidance = tokenizer.decode(outputs[0], skip_special_tokens=True)
        # Extract the part after the prompt
        guidance = guidance.replace(prompt, "").strip()
        navigation_guidances.append(guidance)
        print(f"Generated guidance for {caption}: {guidance}")
    return navigation_guidances


def text_to_speech(captions):
    caption_text = ' '.join(captions)
    # Select a more natural voice if available
    voices = tts_engine.getProperty('voices')
    for voice in voices:
        if 'samantha' in voice.id.lower():  # Example for macOS
            tts_engine.setProperty('voice', voice.id)
            break
    # Adjust rate and volume for natural speech
    tts_engine.setProperty('rate', 150)  # Slower rate
    tts_engine.setProperty('volume', 1.0)  # Max volume
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
