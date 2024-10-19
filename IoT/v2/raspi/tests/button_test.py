import RPi.GPIO as GPIO
import time

# Test setup
GPIO.setmode(GPIO.BOARD)

# Test button setup
TEST_BUTTON_PIN = 11  # Change to an available GPIO pin
GPIO.setup(TEST_BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def test_button_press():
    print("Press the button...")
    button_pressed = False
    start_time = None

    while not button_pressed:
        if GPIO.input(TEST_BUTTON_PIN) == GPIO.LOW:
            if start_time is None:
                start_time = time.time()
            elif time.time() - start_time >= 1:
                button_pressed = True
        else:
            start_time = None
        
        time.sleep(0.1)

    print("Button pressed for 1 second!")

try:
    test_button_press()
except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup()