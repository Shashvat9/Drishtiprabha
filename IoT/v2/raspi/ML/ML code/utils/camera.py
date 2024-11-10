from picamera2 import Picamera2
import numpy as np


picam2 = Picamera2()
picam2.start()

class Camera:
    def __init__(self, resolution=(320, 240)):
        self.picam2 = Picamera2()
        self.config = self.picam2.create_still_configuration(
            main={"size": resolution, "format": "RGB888"}
        )
        self.picam2.configure(self.config)
        self.picam2.start()
        print("Camera initialized with resolution:", resolution)

    def capture_image(self):
        try:
            frame = self.picam2.capture_array()
            if frame is None:
                print("Warning: Captured frame is None.")
                return None
            return frame
        except Exception as e:
            print(f"Error capturing image: {e}")
            return None

    def release_camera(self):
        self.picam2.stop()
        print("Camera released.")

def release_camera():
    # Stop the camera
    picam2.stop()