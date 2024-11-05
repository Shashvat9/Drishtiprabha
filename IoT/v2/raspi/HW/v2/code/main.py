import sys
import os
import time

# Add the utils to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '../utils'))

from buzzer import Buzzer
from button import ButtonHandler
from ultrasonic import Ultrasonic
from request_ec2 import EC2Request
import RPi.GPIO as GPIO
from dotenv import load_dotenv





# Specify the path to the .env file
dotenv_path = os.path.join(os.path.dirname(__file__), '../IoT/v2/raspi/HW/v2/.env')
load_dotenv(dotenv_path)

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
    buzzer = Buzzer(pin=buzzer_pin, frequency=1500)
    button_click_count = 0
    button = ButtonHandler(pin=button_pin)
    ultrasonic_sensor = Ultrasonic(trig_pin=ultrasonic_pin_trig, echo_pin=ultrasonic_pin_echo)
    ec2_request = EC2Request(api_key=api_key_from_env, longitude=72.820095, latitude=22.599911, d_id="3")
    while True:
        distance = ultrasonic_sensor.measure_distance()
        print(f"Distance: {distance} cm")
        buzzer.buzz_control(distance)
        if(button.get_click_count() == 5):
            ec2_request.send_request()
            print("Request sent")
            time.sleep(1)
except Exception as e:
    print(e)
except KeyboardInterrupt:
    print("Cleaning up")
    button.cleanup()
    ultrasonic_sensor.cleanup()
    buzzer.cleanup()
    GPIO.cleanup()
    print("Exiting")