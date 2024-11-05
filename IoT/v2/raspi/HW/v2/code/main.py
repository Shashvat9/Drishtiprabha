import os
import time
from dotenv import load_dotenv
from buzzer import Buzzer
from ultrasonic import Ultrasonic
from button_handler import ButtonHandler
from ec2_request import EC2Request
import RPi.GPIO as GPIO

dotenv_path = '.env'
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