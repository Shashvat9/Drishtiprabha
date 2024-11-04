import RPi.GPIO as GPIO 
import time

class ButtonHandler:
    def __init__(self, pin=11):
        GPIO.setmode(GPIO.BOARD)
        self.TEST_BUTTON_PIN = pin
        GPIO.setup(self.TEST_BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def is_button_pressed(self):
        return GPIO.input(self.TEST_BUTTON_PIN) == GPIO.LOW

    def button_released(self):
        return GPIO.input(self.TEST_BUTTON_PIN) == GPIO.HIGH

    def button_click(self):
        if self.is_button_pressed():
            time.sleep(0.1)
            if self.button_released():
                return True
        return False

    def button_click_count(self, timeout=1.5):
        click_count = 0
        start_time = time.time()
        while True:
            if self.is_button_pressed():
                while self.is_button_pressed():
                    time.sleep(0.05)
                click_count += 1
                time.sleep(0.1)
            if time.time() - start_time >= timeout:
                break
            time.sleep(0.05)
        return click_count

    def press_and_hold(self):
        start_time = time.time()
        while True:
            if self.is_button_pressed():
                if time.time() - start_time >= 2:
                    return True
            else:
                start_time = time.time()
            time.sleep(0.1)
        return False

    def get_click_count(self):
        click_count = 0
        start_time = time.time()
        timeout = 1.5
        hold_time_threshold = 2
        while time.time() - start_time < timeout:
            if self.is_button_pressed():
                press_start = time.time()
                while self.is_button_pressed():
                    time.sleep(0.05)
                    if time.time() - press_start >= hold_time_threshold:
                        return 5
                click_count += 1
                time.sleep(0.1)
            time.sleep(0.05)
        return click_count

    def cleanup(self):
        GPIO.cleanup()

def main():
    button_handler = ButtonHandler()
    try:
        while True:
            event = button_handler.get_click_count()
            print(f"Detected event: {event}")
    except KeyboardInterrupt:
        pass
    finally:
        button_handler.cleanup()

if __name__ == "__main__":
    main()