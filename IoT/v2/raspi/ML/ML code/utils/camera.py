# utils/camera.py

from picamera2 import Picamera2
import cv2

class Camera:
    def __init__(self, resolution=(320, 240)):
        self.picam2 = Picamera2()
        try:
            self.config = self.picam2.create_still_configuration(
                main={"size": resolution, "format": "RGB888"}
            )
            self.picam2.configure(self.config)
            self.picam2.start()
            print("Camera initialized with resolution:", resolution)
        except RuntimeError as e:
            print(f"Failed to initialize camera: {e}")
            self.picam2 = None

    def capture_image(self):
        if not self.picam2:
            print("Camera not initialized.")
            return None
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
        if self.picam2:
            self.picam2.stop()
            print("Camera released.")
            self.picam2 = None