from yolo_detection import detect_objects
from embedding import generate_image_embedding
from navigation import llm_navigation_solution
from text_to_speech import text_to_speech
from utils.ultrasonic_sensor import get_distance
from utils.camera import capture_image

import time

def main():
    while True:
        frame = capture_image() 
        

        detections = detect_objects(frame)
        captions = [f"{obj} at {get_distance()} inches" for obj in detections]

        if captions:
            text_to_speech(captions)
        embedding = generate_image_embedding(frame)
        navigation_instruction = llm_navigation_solution(embedding, captions)
        
        text_to_speech([navigation_instruction])

        time.sleep(0.5)

if __name__ == "__main__":
    main()
