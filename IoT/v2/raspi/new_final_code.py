import RPi.GPIO as GPIO
import time
from request_ec2 import EC2Request

# Board setup
GPIO.setmode(GPIO.BOARD)

# Button setup
BUTTON_PIN = 11
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def check_button_press():
    # Checking if button is pressed for 1 second
    start_time = time.time()
    while GPIO.input(BUTTON_PIN) == GPIO.LOW:
        if time.time() - start_time >= 1:
            # Button pressed for 1 second, send request
            ec2_request = EC2Request(api_key="dp123", longitude=72.820095, latitude=22.599911, d_id="2")
            ec2_request.send_request()
            break

try:
    # Keep the script running
    while True:
        check_button_press()
        time.sleep(0.1)
except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup()