import os
import cv2
from ultralytics import YOLO
import pyttsx3
from threading import Thread
import time
from picamera2 import Picamera2

# Initialize pyttsx3 engine
engine = pyttsx3.init()
engine.setProperty('rate', 130)    # Set speech rate
engine.setProperty('volume', 0.8)  # Set volume level (0.0 to 1.0)

def play_audio(text):
    """Converts text to speech and plays the audio."""
    engine.say(text)
    engine.runAndWait()

def text_to_speech(captions, last_tts_time, cooldown=2):
    """
    Converts captions to speech and plays the audio.
    Implements a cooldown to prevent excessive TTS calls.
    
    Args:
        captions (list): List of detected object names.
        last_tts_time (list): Single-element list tracking the last TTS timestamp.
        cooldown (int): Cooldown period in seconds.
    """
    current_time = time.time()
    if current_time - last_tts_time[0] < cooldown:
        return  # Skip TTS if within cooldown

    if not captions:
        return

    # Combine all captions into a single string
    caption_text = ', '.join(captions)
    print(f"TTS Output: {caption_text}")

    # Play the generated speech in a separate thread
    audio_thread = Thread(target=play_audio, args=(caption_text,))
    audio_thread.start()

    # Update the last TTS time
    last_tts_time[0] = current_time

def run_object_detection():
    """
    Runs the object detection model and handles TTS for detected objects.
    """
    # Load YOLO model (YOLOv8n is lightweight and suitable for Raspberry Pi)
    model = YOLO('yolov8n.pt')  # Ensure the model file is present or download it

    # Initialize Picamera2 with RGB888 format
    picam2 = Picamera2()
    picam2.configure(
        picam2.create_still_configuration(
            main={"size": (640, 480), "format": "RGB888"}
        )
    )
    picam2.start()
    time.sleep(2)  # Allow camera to warm up

    # Initialize TTS cooldown tracker
    last_tts_time = [0]  # Using a list to allow mutable reference

    try:
        while True:
            # Capture frame as a numpy array
            frame = picam2.capture_array()

            if frame is None:
                print("Failed to capture frame.")
                break

            # Resize frame for faster processing
            frame_resized = cv2.resize(frame, (640, 480))

            # **Convert from BGRA to BGR if necessary**
            if frame_resized.shape[2] == 4:
                frame_resized = cv2.cvtColor(frame_resized, cv2.COLOR_BGRA2BGR)

            # Perform object detection
            results = model(frame_resized)

            captions = []
            for result in results:
                for detection in result.boxes:
                    class_id = int(detection.cls)
                    class_name = model.names[class_id]
                    captions.append(class_name)

            # Trigger TTS if any objects are detected
            if captions:
                text_to_speech(captions, last_tts_time, cooldown=2)  # 2-second cooldown

    except KeyboardInterrupt:
        print("Interrupted by user.")

    finally:
        # Release resources
        picam2.stop()
        engine.stop()

if __name__ == "__main__":
    run_object_detection()