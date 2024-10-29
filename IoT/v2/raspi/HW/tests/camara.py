import time
from picamera import PiCamera

def test_camera():
    try:
        # Initialize the camera
        camera = PiCamera()
        
        # Camera warm-up time
        time.sleep(2)
        
        # Capture an image
        image_path = '/home/pi/test_image.jpg'  # Change the path as needed
        camera.capture(image_path)
        
        print(f"Image captured and saved to {image_path}")
        
    except Exception as e:
        print(f"An error occurred: {e}")
        
    finally:
        # Clean up resources
        camera.close()

if __name__ == "__main__":
    test_camera()