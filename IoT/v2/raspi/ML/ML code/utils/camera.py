from picamera2 import Picamera2
import numpy as np


picam2 = Picamera2()
picam2.start()

def capture_image():
    # Capture image as a NumPy array
    frame = picam2.capture_array()
    return frame

def release_camera():
    # Stop the camera
    picam2.stop()