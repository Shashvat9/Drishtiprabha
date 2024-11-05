from picamera2 import Picamera2
import time

picam2 = Picamera2()
picam2.start_preview()
time.sleep(2)  # Allow camera to warm up
picam2.capture_file("test_picamera2.jpg")
print("Image captured as test_picamera2.jpg")