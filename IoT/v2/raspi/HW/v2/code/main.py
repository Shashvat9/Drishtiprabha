"""
    Main code for the Raspberry Pi
"""
import os
import time
import sys
import RPi.GPIO as GPIO
from threading import Event

# Add the path to the utils folder
sys.path.append(os.path.join(os.path.dirname(__file__), '../utils'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../IoT/v2/raspi/ML'))

# Import the required modules
# from app import run_ml_model  # Import the ML function
from dotenv import load_dotenv
from buzzer import Buzzer
from ultrasonic import Ultrasonic
from button import ButtonHandler
from request_ec2 import EC2Request

# Set the GPIO mode
GPIO.setmode(GPIO.BOARD)


# Load env
dotenv_path = '/home/admin/Drishtiprabha/IoT/v2/raspi/HW/v2/.env'
# print(f"Dotenv path: {dotenv_path}")
# print("File exists:", os.path.isfile(dotenv_path))
# print("Readable:", os.access(dotenv_path, os.R_OK))
load_dotenv(dotenv_path)

# Get API_KEY from .env
api_key_from_env = os.getenv("API_KEY")
# api_key_from_env = "dp123"

# Pin setup
button_pin = 11
buzzer_pin = 37
ultrasonic_pin_trig = 15
ultrasonic_pin_echo = 16

# Global variables
is_button_pressed = False
stop_ml = Event()  # Event to signal ML model to stop

print(os.path.join(os.path.dirname(__file__), '../IoT/v2/raspi/ML'))

while True:
    """
        this if statement will work with HW and EC2 request 
        if the button is pressed once
            then the loop will break and is_button_pressed will be set to True which will stop the loop and the program will enter in ML block
    """
    if not is_button_pressed:
        try:
            # Initialize the buzzer, button, ultrasonic sensor, and EC2 request objects
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
                if click_count == 1:
                    is_button_pressed = True
                    stop_ml.set()  # Signal ML model to stop if running
                    break
                elif click_count == 5:
                    ec2_request.send_request()
        except Exception as e:
            print(e)
        finally:
            # Cleanup the GPIO pins
            buzzer.cleanup()
            button.cleanup()
            ultrasonic_sensor.cleanup()
            GPIO.cleanup()
    elif is_button_pressed:
        # Start the ML model
        run_ml_model(stop_ml)
        # After ML model finishes
        break  # Exit the main loop or implement further logic as needed