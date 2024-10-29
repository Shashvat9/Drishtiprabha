from ultralytics import YOLO
from gtts import gTTS
import os
import cv2
# from libcamera import controls
from picamera2 import Picamera2, Preview

# Load YOLOv8 model (Nano version for testing)
model = YOLO('yolov8n.pt') 

# Initialize the camera
picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration(main={"format": 'XRGB8888', "size": (640, 480)}))
picam2.start()

def text_to_speech(captions):
    # Convert captions to a single string
    caption_text = ' '.join(captions)
    
    # Generate speech using Google TTS
    tts = gTTS(text=caption_text, lang='en')
    
    # Save the speech to an MP3 file
    tts.save("caption_audio.mp3")
    
    # Play the generated speech (replace with your preferred audio player if needed)
    os.system("mpg321 caption_audio.mp3") 

while True:
    frame = picam2.capture_array()

    # Convert the frame to RGB format
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
    
    # Run YOLOv8 object detection on the frame
    results = model(frame_rgb)

    # Generate captions from detections
    captions = []
    for result in results:
        for detection in result.boxes:
            class_name = model.names[int(detection.cls)] 
            captions.append(f"Detected {class_name}")

    # Convert the captions to speech and play the audio
    if captions:
        text_to_speech(captions)

    # Display the frame with YOLOv8 detections
    cv2.imshow("YOLOv8 Detection", frame_rgb)

    # Press 'q' to exit the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
picam2.stop()
cv2.destroyAllWindows()