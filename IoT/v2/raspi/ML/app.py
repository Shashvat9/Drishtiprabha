import os
import cv2
from ultralytics import YOLO
from gtts import gTTS
from threading import Thread, Event
import time
from picamera2 import Picamera2
import hashlib

class ObjectDetectionModel:
    def __init__(self, cooldown=2):
        """
        Initializes the object detection model and TTS components.
        
        Args:
            cooldown (int): Cooldown period in seconds between TTS calls.
        """
        self.model = YOLO('yolov8n.pt')  # Ensure the model file is present or download it
        self.picam2 = Picamera2()
        self.picam2.configure(
            self.picam2.create_still_configuration(
                main={"size": (640, 480), "format": "RGB888"}
            )
        )
        self.cooldown = cooldown
        self.last_tts_time = [0]  # Using a list to allow mutable reference
        self.running = False
        self.thread = None
        self.stop_event = Event()

    def play_audio_gtts(self, text):
        """Converts text to speech using gTTS and plays the audio using mpg321."""
        try:
            # Generate a unique filename based on the text
            filename_hash = hashlib.md5(text.encode()).hexdigest()
            audio_file = f"tts_cache/{filename_hash}.mp3"

            # Create cache directory if it doesn't exist
            os.makedirs("tts_cache", exist_ok=True)

            # Check if the audio file already exists
            if not os.path.isfile(audio_file):
                tts = gTTS(text=text, lang='en')
                tts.save(audio_file)

            # Play the cached audio file using mpg321
            os.system(f"mpg321 {audio_file}")
            
            # Optionally, remove the audio file after playback to save space
            # os.remove(audio_file)
        except Exception as e:
            print(f"Error in play_audio_gtts: {e}")

    def text_to_speech(self, captions):
        """
        Converts captions to speech and plays the audio.
        Implements a cooldown to prevent excessive TTS calls.
        
        Args:
            captions (list): List of detected object names.
        """
        current_time = time.time()
        if current_time - self.last_tts_time[0] < self.cooldown:
            return  # Skip TTS if within cooldown

        if not captions:
            return

        # Combine all captions into a single string with proper punctuation
        caption_text = ', '.join(captions) + '.'
        print(f"TTS Output: {caption_text}")

        # Play the generated speech in a separate thread
        audio_thread = Thread(target=self.play_audio_gtts, args=(caption_text,))
        audio_thread.start()

        # Update the last TTS time
        self.last_tts_time[0] = current_time

    def run_object_detection(self):
        """
        Runs the object detection model and handles TTS for detected objects.
        Runs in a separate thread.
        """
        self.picam2.start()
        time.sleep(2)  # Allow camera to warm up

        try:
            while not self.stop_event.is_set():
                # Capture frame as a numpy array
                frame = self.picam2.capture_array()

                if frame is None:
                    print("Failed to capture frame.")
                    continue

                # Resize frame for faster processing
                frame_resized = cv2.resize(frame, (640, 480))

                # Convert from BGRA to BGR if necessary
                if frame_resized.shape[2] == 4:
                    frame_resized = cv2.cvtColor(frame_resized, cv2.COLOR_BGRA2BGR)

                # Perform object detection
                results = self.model(frame_resized)

                captions = []
                for result in results:
                    for detection in result.boxes:
                        class_id = int(detection.cls)
                        class_name = self.model.names[class_id]
                        captions.append(class_name)

                # Trigger TTS if any objects are detected
                if captions:
                    self.text_to_speech(captions)

                # Small delay to reduce CPU usage
                time.sleep(0.5)

        except Exception as e:
            print(f"Error in run_object_detection: {e}")

        finally:
            self.picam2.stop()
            print("Object detection stopped.")

    def start(self):
        """Starts the object detection in a separate thread."""
        if not self.running:
            self.running = True
            self.stop_event.clear()
            self.thread = Thread(target=self.run_object_detection, daemon=True)
            self.thread.start()
            print("Object detection started.")

    def stop(self):
        """Stops the object detection."""
        if self.running:
            self.stop_event.set()
            self.thread.join()
            self.running = False
            print("Object detection stopped.")

def main():
    # Example usage
    od_model = ObjectDetectionModel(cooldown=2)
    od_model.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Interrupted by user.")
    finally:
        od_model.stop()

if __name__ == "__main__":
    main()