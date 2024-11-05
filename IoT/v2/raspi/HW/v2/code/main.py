import os
import sys
import RPi.GPIO as GPIO
import time

# Add the path to the utils and ML folders if needed
sys.path.append(os.path.join(os.path.dirname(__file__), '../utils'))
sys.path.append('/home/admin/Drishtiprabha/IoT/v2/raspi/ML')

from threading import Thread, Timer
from app import ObjectDetectionModel  # Import the ML class
from dotenv import load_dotenv
from buzzer import Buzzer
from ultrasonic import Ultrasonic
from request_ec2 import EC2Request



# Load environment variables
dotenv_path = '/home/admin/Drishtiprabha/IoT/v2/raspi/HW/v2/.env'
load_dotenv(dotenv_path)

# Get API_KEY from .env
api_key_from_env = os.getenv("API_KEY")
# api_key_from_env = "dp123"  # Uncomment for testing without .env

# Pin setup
button_pin = 11
buzzer_pin = 37
ultrasonic_pin_trig = 15
ultrasonic_pin_echo = 16

# Global variables for press detection
press_count = 0
press_timer = None
DOUBLE_PRESS_INTERVAL = 0.5  # 300 milliseconds

# Global variable to track ML model state
ml_active = False

# Initialize GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Button with pull-up resistor

# Initialize hardware components
buzzer = Buzzer(buzzer_pin)
ultrasonic = Ultrasonic(ultrasonic_pin_trig, ultrasonic_pin_echo)

# Initialize ML model
ml_model = ObjectDetectionModel(cooldown=2)

def button_callback(channel):
    global ml_active, press_count, press_timer

    press_count += 1

    if press_timer is not None:
        press_timer.cancel()

    press_timer = Timer(DOUBLE_PRESS_INTERVAL, handle_press, args=[press_count])
    press_timer.start()

def handle_press(count):
    global ml_active, press_count, press_timer

    if count == 1:
        # Single Press: Toggle ML Model
        if ml_active:
            print("Button pressed: Stopping ML model.")
            ml_model.stop()
            ml_active = False
            buzzer.beep_short()  # Indicate state change
        else:
            print("Button pressed: Starting ML model.")
            ml_model.start()
            ml_active = True
            buzzer.beep_long()  # Indicate state change
    elif count == 2:
        # Double Press: Trigger EC2 Request
        print("Button double-pressed: Sending EC2 request.")
        buzzer.beep_double()  # Audible feedback for double press
        if api_key_from_env:
            ec2_request = EC2Request(api_key=api_key_from_env, longitude=72.820095, latitude=22.599911, d_id="2")
            ec2_request.send_request()

    # Reset press_count and press_timer
    press_count = 0
    press_timer = None

def main_loop():
    try:
        # Setup button interrupt
        GPIO.add_event_detect(button_pin, GPIO.FALLING, callback=button_callback, bouncetime=200)
        print(api_key_from_env)

        while True:
            # Example: Ultrasonic sensor reading
            distance = ultrasonic.measure_distance()
            print(f"Distance: {distance} cm")
            buzzer.buzz_control(distance)
            # if distance < 10:
            #     buzzer.beep()
            #     # Example action: Send request to EC2 if API_KEY is set
            #     if api_key_from_env:
            #         ec2_request = EC2Request(api_key=api_key_from_env)
            #         ec2_request.send_alert(distance)
            time.sleep(0.2)

    except KeyboardInterrupt:
        print("Interrupted by user.")

    finally:
        # Cleanup
        GPIO.cleanup()
        if ml_active:
            ml_model.stop()

if __name__ == "__main__":
    main_loop()