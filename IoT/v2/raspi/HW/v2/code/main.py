import os
import time
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '../utils'))

from dotenv import load_dotenv
from buzzer import Buzzer
from ultrasonic import Ultrasonic
from button import ButtonHandler
from request_ec2 import EC2Request
import RPi.GPIO as GPIO

# Add to main.py to verify the dotenv path and permissions
# import os

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
print(f"Dotenv path: {dotenv_path}")
print("File exists:", os.path.isfile(dotenv_path))
print("Readable:", os.access(dotenv_path, os.R_OK))
load_dotenv(dotenv_path)

dotenv_path = os.path.join(os.path.dirname(__file__))
# load_dotenv(dotenv_path)

# get key
api_key_from_env = os.getenv("API_KEY")
# api_key_from_env = "dp123"

GPIO.setmode(GPIO.BOARD)

# pin setup
button_pin = 11
buzzer_pin = 37
ultrasonic_pin_trig = 15
ultrasonic_pin_echo = 16

try:
    print(api_key_from_env)
    buzzer = Buzzer(pin=buzzer_pin, frequency=2000)
    button = ButtonHandler(pin=button_pin)
    ultrasonic_sensor = Ultrasonic(trig_pin=ultrasonic_pin_trig, echo_pin=ultrasonic_pin_echo)
    ec2_request = EC2Request(api_key=api_key_from_env, longitude=72.820095, latitude=22.599911, d_id="2")
    
    while True:
        distance = ultrasonic_sensor.measure_distance()
        print(f"Distance: {distance} cm")
        buzzer.buzz_control(distance)
        time.sleep(0.1)
        
        click_count = button.get_click_count()
        if click_count > 0:
            print(f"Button Clicked: {click_count} times")
            # if click_count == 5:
            #     ec2_request.send_request()
            #     print("Request sent")
except Exception as e:
    print(e)
except KeyboardInterrupt:
    print("Cleaning up")
    button.cleanup()
    ultrasonic_sensor.cleanup()
    buzzer.cleanup()
    GPIO.cleanup()
    print("Exiting")