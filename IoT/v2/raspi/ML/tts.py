from ultralytics import YOLO

model = YOLO('yolov11s.pt')  # Consider using a smaller model like 'yolov11s.pt'
from espeak import synthesize
import picamera

def text_to_speech(text):
  synthesize(text)

while True:
  with picamera.PiCamera() as camera:
    camera.resolution = (640, 480)  # Adjust resolution as needed
    camera.capture_continuous('image.jpg', format='jpeg', use_video_port=True)
    break

  image = cv2.imread('image.jpg')
  
  results = model(image)

  captions = []
  for result in results.pandas().xyxy[0]:  #
    class_name = result['name']
    captions.append(f"Detected {class_name}")


  if captions:
    text_to_speech(' '.join(captions))  # Combine captions for single speech

 
  os.remove('image.jpg')

  user_input = input("Press 'q' to quit, any other key to continue: ")
  if user_input.lower() == 'q':
    break