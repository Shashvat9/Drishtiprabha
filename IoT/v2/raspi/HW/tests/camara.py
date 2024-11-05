import cv2

def test_camera(camera_index):
    cap = cv2.VideoCapture(camera_index)
    if not cap.isOpened():
        print(f"Camera at index {camera_index} could not be opened.")
        return False
    ret, frame = cap.read()
    if ret:
        print(f"Camera at index {camera_index} is working.")
    else:
        print(f"Camera at index {camera_index} failed to capture a frame.")
    cap.release()
    return ret

if __name__ == "__main__":
    for index in range(5):
        print(f"Testing camera index {index}:")
        success = test_camera(index)
        if success:
            print(f"--> Camera index {index} is available.\n")
        else:
            print(f"--> Camera index {index} is not available.\n")