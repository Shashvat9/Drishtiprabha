# import os
# import sys
# import RPi.GPIO as GPIO
# import time

# # Add the path to the utils and ML folders if needed
# sys.path.append(os.path.join(os.path.dirname(__file__), '../utils'))
# sys.path.append('/home/admin/Drishtiprabha/IoT/v2/raspi/ML')

# from threading import Thread, Timer, Lock
# from app import ObjectDetectionModel  # Import the ML class
# from dotenv import load_dotenv
# # from smallBuzzer import Buzzer
# from buzzer import Buzzer
# from ultrasonic import Ultrasonic
# from request_ec2 import EC2Request




# # Load environment variables
# dotenv_path = '/home/admin/Drishtiprabha/IoT/v2/raspi/HW/v2/.env'
# load_dotenv(dotenv_path)

# # Get API_KEY from .env
# api_key_from_env = os.getenv("API_KEY")
# # api_key_from_env = "dp123"  # Uncomment for testing without .env

# # Pin setup
# button_pin = 11
# buzzer_pin = 37
# ultrasonic_pin_trig = 15
# ultrasonic_pin_echo = 16

# # Global variables for press detection
# press_count = 0
# press_timer = None
# DOUBLE_PRESS_INTERVAL = 0.3  # 300 milliseconds

# # Global variable to track ML model state
# ml_active = False

# # Initialize GPIO
# GPIO.setmode(GPIO.BOARD)
# GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Button with pull-up resistor

# # Initialize hardware components
# buzzer = Buzzer(buzzer_pin)
# ultrasonic = Ultrasonic(ultrasonic_pin_trig, ultrasonic_pin_echo)

# # Initialize ML model
# ml_model = ObjectDetectionModel(cooldown=2)

# # Initialize a lock for thread-safe operations
# lock = Lock()

# def button_callback(channel):
#     global press_count, press_timer

#     with lock:
#         press_count += 1
#         print(f"Button pressed. Current press count: {press_count}")

#         if press_timer is not None:
#             press_timer.cancel()

#         press_timer = Timer(DOUBLE_PRESS_INTERVAL, handle_press, args=[press_count])
#         press_timer.start()

# def handle_press(count):
#     global ml_active, press_count, press_timer

#     with lock:
#         print(f"Handling press. Count received: {count}")

#         if count == 1:
#             # Single Press: Toggle ML Model
#             if ml_active:
#                 print("Button pressed: Stopping ML model.")
#                 ml_model.stop()
#                 ml_active = False
#                 buzzer.beep_short()  # Indicate state change
#             else:
#                 print("Button pressed: Starting ML model.")
#                 ml_model.start()
#                 ml_active = True
#                 buzzer.beep_long()  # Indicate state change
#         elif count >= 2:
#             # Double Press: Trigger EC2 Request
#             print("Button double-pressed: Sending EC2 request.")
#             buzzer.beep_request_ec2()  # Audible feedback for double press
#             # if api_key_from_env:
#             ec2_request = EC2Request(api_key=api_key_from_env, longitude=72.819836, latitude=22.600959, d_id="2")
#             # ec2_request = EC2Request(api_key=api_key_from_env, longitude=72.819309, latitude=22.605796, d_id="2")
#             ec2_request.send_request()
#             time.sleep(1)

#         # Reset press_count and press_timer
#         press_count = 0
#         press_timer = None

# def main_loop():
#     try:
#         # Setup button interrupt
#         GPIO.add_event_detect(button_pin, GPIO.FALLING, callback=button_callback, bouncetime=200)

#         while True:
#             # Example: Ultrasonic sensor reading
#             distance = ultrasonic.measure_distance()
#             print(f"Distance: {distance} cm")
#             buzzer.buzz_control(distance)
#             time.sleep(0.1)

#     except KeyboardInterrupt:
#         print("Interrupted by user.")

#     finally:
#         # Cleanup
#         GPIO.cleanup()
#         with lock:
#             if ml_active:
#                 ml_model.stop()

# if __name__ == "__main__":
#         main_loop()

# main.py (Migrated to gpiozero)

import os
import sys
# Removed RPi.GPIO import
import time

# Import necessary gpiozero classes
from gpiozero import Button # For the button input
# Optional: Force recommended pin factory for Pi 5
from gpiozero import Device
from gpiozero.pins.lgpio import LGPIOFactory
# Device.pin_factory = LGPIOFactory()

# Add the path to the utils and ML folders if needed
sys.path.append(os.path.join(os.path.dirname(__file__), '../utils'))
sys.path.append('/home/admin/Drishtiprabha/IoT/v2/raspi/ML')

from threading import Thread, Timer, Lock
from app import ObjectDetectionModel  # Import the ML class
from dotenv import load_dotenv
# from smallBuzzer import Buzzer # Assuming buzzer.py is correct now
from buzzer import Buzzer # Use the migrated buzzer
from ultrasonic import Ultrasonic # Use the migrated ultrasonic
from request_ec2 import EC2Request
# Import signal for pause() if changing main loop structure, but not needed yet
# from signal import pause


# Load environment variables
dotenv_path = '/home/admin/Drishtiprabha/IoT/v2/raspi/HW/v2/.env'
load_dotenv(dotenv_path)

# Get API_KEY from .env
api_key_from_env = os.getenv("API_KEY")
# api_key_from_env = "dp123"  # Uncomment for testing without .env

# --- Pin setup (Using BCM numbering now) ---
# BOARD 11 -> BCM 17
button_pin_bcm = 17
# BOARD 37 -> BCM 26
buzzer_pin_bcm = 26
# BOARD 15 -> BCM 22
ultrasonic_pin_trig_bcm = 22
# BOARD 16 -> BCM 23
ultrasonic_pin_echo_bcm = 23

# Global variables for press detection
press_count = 0
press_timer = None
DOUBLE_PRESS_INTERVAL = 0.3  # 300 milliseconds

# Global variable to track ML model state
ml_active = False

# Initialize GPIO - Not needed with gpiozero


# --- Initialize hardware components using gpiozero classes/updated classes ---
try:
    # Button with internal pull-up enabled, uses BCM pin
    # Default bounce_time is None (handled differently), hold_time for long press
    button = Button(button_pin_bcm, pull_up=True,bounce_time=0.1)

    # Initialize using migrated classes with BCM pins
    buzzer = Buzzer(buzzer_pin_bcm)
    ultrasonic = Ultrasonic(ultrasonic_pin_trig_bcm, ultrasonic_pin_echo_bcm)
except Exception as e:
    print(f"Fatal Error initializing hardware: {e}")
    print("Check pin numbers (BCM), connections, permissions, and ensure libraries (gpiozero, lgpio) are installed.")
    sys.exit(1) # Exit if hardware can't be initialized

# Initialize ML model
ml_model = ObjectDetectionModel(cooldown=2)

# Initialize a lock for thread-safe operations
lock = Lock()

# --- Button Callback Logic (Adapted for gpiozero) ---
# NOTE: The 'channel' argument is removed as gpiozero doesn't pass it by default
def button_callback():
    global press_count, press_timer

    # Debouncing is handled somewhat internally by Button,
    # but this timer logic adds specific double-press detection.
    with lock:
        press_count += 1
        print(f"Button pressed. Current press count: {press_count}")

        if press_timer is not None:
            press_timer.cancel()

        # Start timer with current press_count
        # If another press comes within DOUBLE_PRESS_INTERVAL,
        # this timer will be cancelled and restarted by the next call.
        # If no other press comes, handle_press runs after the interval.
        press_timer = Timer(DOUBLE_PRESS_INTERVAL, handle_press, args=[press_count])
        press_timer.start()

def handle_press(count_at_timeout):
    global ml_active, press_count, press_timer
    current_total_presses = 0

    # We need to read the *final* press_count safely when the timer expires
    with lock:
        current_total_presses = press_count
        # Reset press count immediately after reading it inside the handler
        press_count = 0
        press_timer = None # Timer has finished or been cancelled implicitly

    print(f"Handling press. Count when timer started: {count_at_timeout}. Total presses detected: {current_total_presses}")

    # Decision is based on the total presses accumulated before the timer fired
    if current_total_presses == 1:
        # Single Press: Toggle ML Model
        with lock: # Lock needed for accessing shared ml_active
            if ml_active:
                print("Button single press: Stopping ML model.")
                ml_model.stop()
                ml_active = False
                buzzer.beep_short()  # Indicate state change
            else:
                print("Button single press: Starting ML model.")
                ml_model.start()
                ml_active = True
                buzzer.beep_long()  # Indicate state change
    elif current_total_presses >= 2:
        # Double Press (or more within interval): Trigger EC2 Request
        print(f"Button multi-press ({current_total_presses}): Sending EC2 request.")
        buzzer.beep_request_ec2()  # Audible feedback for double press
        # if api_key_from_env: # Ensure API key exists before creating request
        ec2_request = EC2Request(api_key=api_key_from_env, longitude=72.819836, latitude=22.600959, d_id="2")
        # ec2_request = EC2Request(api_key=api_key_from_env, longitude=72.819309, latitude=22.605796, d_id="2")
        ec2_request.send_request()
        # Consider running send_request in a thread if it blocks for long
        time.sleep(0.1) # Short delay after request if needed

    # else: # Handle cases if needed, e.g., count_at_timeout was 0 but shouldn't happen

# --- Main Loop ---
def main_loop():
    global ml_active # Ensure access if needed inside loop (though seems managed by button)

    try:
        # --- Setup button event detection using gpiozero ---
        # Assign the callback function to the button's when_pressed event
        button.when_pressed = button_callback
        # Button also has when_released, when_held if needed

        print("System initialized.")
        # print(f"Using BCM pins - Button: {button_pin_bcm}, Buzzer: {buzzer_pin_bcm}, US Trig: {ultrasonic_pin_trig_bcm}, US Echo: {ultrasonic_pin_echo_bcm}")

        # Keep the main loop for periodic tasks like ultrasonic reading
        while True:
            # Ultrasonic sensor reading
            distance = ultrasonic.measure_distance()

            # Optional: Add check for error code from sensor
            if distance != 99999:
                print(f"Distance: {distance:.2f} cm")
                # Control buzzer based on distance using the migrated class method
                buzzer.buzz_control(distance)
            else:
                print("Ultrasonic sensor read error or timeout.")

            # Let the CPU rest a bit, prevents 100% CPU usage
            time.sleep(0.2) # Slightly longer sleep might be fine

    except KeyboardInterrupt:
        print("\nInterrupted by user. Cleaning up...")

    finally:
        # Cleanup - Release resources
        print("Performing final cleanup...")
        with lock: # Ensure thread safety for ML model stop
            if ml_active:
                print("Stopping ML model...")
                ml_model.stop()
        # Close gpiozero devices explicitly (good practice)
        if 'button' in globals() and button:
             button.close()
        if 'buzzer' in globals() and buzzer:
             buzzer.close()
        if 'ultrasonic' in globals() and ultrasonic:
             ultrasonic.close()

        # GPIO.cleanup() is no longer needed here; gpiozero handles it.
        print("Cleanup complete. Exiting.")


if __name__ == "__main__":
    main_loop()