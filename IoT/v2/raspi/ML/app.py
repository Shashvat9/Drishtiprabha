import os
import cv2
from ultralytics import YOLO
from gtts import gTTS
import pygame
from threading import Thread
import time
from picamera2 import Picamera2

# Initialize Pygame Mixer for audio playback
pygame.mixer.init()

def play_audio(file_path):
    """Plays the specified audio file."""
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

def text_to_speech(captions):
    """
    Converts captions to speech and plays the audio.
    """
    if not captions:
        return

    # Combine all captions into a single string
    caption_text = ' '.join(captions)
    print(f"TTS Output: {caption_text}")

    # Generate speech using gTTS
    tts = gTTS(text=caption_text, lang='en')
    audio_file = "caption_audio.mp3"
    tts.save(audio_file)

    # Play the generated speech in a separate thread
    audio_thread = Thread(target=play_audio, args=(audio_file,))
    audio_thread.start()

def run_object_detection():
    """
    Runs the object detection model and handles TTS for detected objects.
    """
    # Load YOLO model (YOLOv8n is lightweight and suitable for Raspberry Pi)
    model = YOLO('yolov8n.pt')  # Ensure the model file is present or download it

    # Initialize Picamera2
    picam2 = Picamera2()
    picam2.configure(picam2.create_preview_configuration(main={"size": (640, 480)}))
    picam2.start()
    time.sleep(2)  # Allow camera to warm up

    # Check if a display is available for cv2.imshow
    display_available = os.environ.get('DISPLAY') is not None

    try:
        while True:
            # Capture frame as a numpy array
            frame = picam2.capture_array()

            if frame is None:
                print("Failed to capture frame.")
                break

            # Resize frame for faster processing
            frame_resized = cv2.resize(frame, (640, 480))

            # Perform object detection
            results = model(frame_resized)

            captions = []
            for result in results:
                for detection in result.boxes:
                    class_id = int(detection.cls)
                    class_name = model.names[class_id]
                    captions.append(f"Detected {class_name}")

                    # Draw bounding box and label on the frame
                    x1, y1, x2, y2 = map(int, detection.xyxy[0])
                    cv2.rectangle(frame_resized, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.putText(frame_resized, class_name, (x1, y1 - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36,255,12), 2)

            # Display the frame with detections if a display is available
            if display_available:
                cv2.imshow("YOLOv8 Detection", frame_resized)

            # Trigger TTS if any objects are detected
            if captions:
                text_to_speech(captions)

            # Exit on pressing 'q' if a display is available
            if display_available:
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

            # Optional: Sleep to reduce CPU usage
            time.sleep(0.1)

    except KeyboardInterrupt:
        print("Interrupted by user.")

    finally:
        # Release resources
        picam2.stop()
        if display_available:
            cv2.destroyAllWindows()
        pygame.mixer.quit()

if __name__ == "__main__":
    run_object_detection()