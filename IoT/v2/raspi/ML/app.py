from ultralytics import YOLO
from gtts import gTTS
import os
import cv2

# Load YOLOv8 model (Nano version for testing)
model = YOLO('yolov8n.pt') 

# Initialize the camera using OpenCV
cap = cv2.VideoCapture(0)  # 0 is the default camera

def text_to_speech(captions):
    # Convert captions to a single string
    caption_text = ' '.join(captions)
    
    # Generate speech using Google TTS
    tts = gTTS(text=caption_text, lang='en')
    
    # Save the speech to an MP3 file
    tts.save("caption_audio.mp3")
    
    # Play the generated speech
    os.system("mpg321 caption_audio.mp3") 

def run_ml_model(stop_event):
    while not stop_event.is_set():
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture image")
            break

        # Convert the frame to RGB format
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
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

        # Check for 'q' key press to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            stop_event.set()
            break

    # Release resources
    cap.release()
    cv2.destroyAllWindows()