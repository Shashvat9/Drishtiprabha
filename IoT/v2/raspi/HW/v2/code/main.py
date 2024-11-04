# Add the utils to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '../utils'))

from buzzer import Buzzer
from button import ButtonHandler
from ultrasonic import Ultrasonic
from request_ec2 import EC2Request
import time
import RPi.GPIO as GPIO
from dotenv import load_dotenv
import os
import sys



# load environment variables
load_dotenv()

# get key
api_key_from_env = os.getenv("API_KEY")

GPIO.setmode(GPIO.BOARD)

# pin setup
button_pin = 11
buzzer_pin = 37
ultrasonic_pin_trig = 15
ultrasonic_pin_echo = 16



try:
    buzzer = Buzzer(pin=buzzer_pin, frequency=1500)
    button_click_count = 0
    button = ButtonHandler(pin=button_pin)
    ultrasonic_sensor = Ultrasonic(trig_pin=ultrasonic_pin_trig, echo_pin=ultrasonic_pin_echo)
    ec2_request = EC2Request()
    while True:
        distance = ultrasonic_sensor.measure_distance()
        print(f"Distance: {distance} cm")
        buzzer.buzz_control(distance)
        if(button.get_click_count() == 5):
            ec2_request.send_request(api_key=api_key_from_env, longitude=72.820095, latitude=22.599911, d_id="2")
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