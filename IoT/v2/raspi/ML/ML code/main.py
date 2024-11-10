# main.py

from yolo_detection import detect_objects
from embedding import generate_image_embedding
from navigation import llm_navigation_solution
from text_to_speech import text_to_speech
from utils.ultrasonic_sensor import get_distance
from utils.camera import Camera

import time

def main():
    camera = Camera(resolution=(320, 240))
    
    try:
        while True:
            frame = camera.capture_image()
            
            if frame is None:
                print("Skipping iteration due to capture failure.")
                time.sleep(0.5)
                continue
            
            detections = detect_objects(frame)
            captions = [f"{obj} at {get_distance()} inches" for obj in detections]

            if captions:
                text_to_speech(captions)
            
            embedding = generate_image_embedding(frame)
            navigation_instruction = llm_navigation_solution(embedding, captions)
            
            text_to_speech([navigation_instruction])

            time.sleep(0.5)
    except KeyboardInterrupt:
        print("Terminating program.")
    finally:
        camera.release_camera()

if __name__ == "__main__":
    main()