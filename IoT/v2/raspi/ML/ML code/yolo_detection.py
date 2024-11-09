from ultralytics import YOLO

model = YOLO('yolov8n.pt') 

def detect_objects(frame):
    results = model(frame)
    return [model.names[int(d.cls)] for result in results for d in result.boxes]
