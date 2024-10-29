import RPi.GPIO as GPIO 
import time

# Test setup
GPIO.setmode(GPIO.BOARD)

# Test button setup
TEST_BUTTON_PIN = 11  # Change to an available GPIO pin
GPIO.setup(TEST_BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def press_and_hold_5_seconds():
    start_time = None
    while True:
        if GPIO.input(TEST_BUTTON_PIN) == GPIO.LOW:
            if start_time is None:
                start_time = time.time()
            elif time.time() - start_time >= 5:
                print("Button pressed and held for 5 seconds!")
                return True
        else:
            start_time = None
        time.sleep(0.1)
    return False

def double_press():
    press_count = 0
    last_press_time = None
    while press_count < 2:
        if GPIO.input(TEST_BUTTON_PIN) == GPIO.LOW:
            if last_press_time is None or time.time() - last_press_time > 0.5:
                press_count += 1
                last_press_time = time.time()
                while GPIO.input(TEST_BUTTON_PIN) == GPIO.LOW:
                    time.sleep(0.1)  # Wait for button release
        time.sleep(0.1)
    if press_count == 2:
        print("Button double pressed!")
        return True
    return False

def triple_press():
    press_count = 0
    last_press_time = None
    while press_count < 3:
        if GPIO.input(TEST_BUTTON_PIN) == GPIO.LOW:
            if last_press_time is None or time.time() - last_press_time > 0.5:
                press_count += 1
                last_press_time = time.time()
                while GPIO.input(TEST_BUTTON_PIN) == GPIO.LOW:
                    time.sleep(0.1)  # Wait for button release
        time.sleep(0.1)
    if press_count == 3:
        print("Button triple pressed!")
        return True
    return False

def main():
    try:
        while True:
            if press_and_hold_5_seconds():
                print("Detected: Press and hold for 5 seconds")
            elif double_press():
                print("Detected: Double press")
            elif triple_press():
                print("Detected: Triple press")
            time.sleep(1)  # Delay before next detection cycle
    except KeyboardInterrupt:
        pass
    finally:
        GPIO.cleanup()

if __name__ == "__main__":
    main()