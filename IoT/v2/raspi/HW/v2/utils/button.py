import RPi.GPIO as GPIO
import time
import threading

class ButtonHandler:
    def __init__(self, pin=11):
        GPIO.setmode(GPIO.BOARD)
        self.TEST_BUTTON_PIN = pin
        GPIO.setup(self.TEST_BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        self.click_count = 0
        self.last_click_time = time.time()
        self.hold_detected = False
        self.lock = threading.Lock()
        GPIO.add_event_detect(self.TEST_BUTTON_PIN, GPIO.BOTH, callback=self._handle_event, bouncetime=50)
        self.hold_timer = None

    def _handle_event(self, channel):
        if GPIO.input(self.TEST_BUTTON_PIN) == GPIO.LOW:
            self.press_time = time.time()
            if self.hold_timer is None:
                self.hold_timer = threading.Timer(2, self._detect_hold)
                self.hold_timer.start()
        else:
            release_time = time.time()
            if self.hold_timer is not None:
                self.hold_timer.cancel()
                self.hold_timer = None
            if not self.hold_detected:
                with self.lock:
                    self.click_count += 1
            self.hold_detected = False

    def _detect_hold(self):
        with self.lock:
            self.click_count = 5
            self.hold_detected = True

    def get_click_count(self):
        with self.lock:
            count = self.click_count
            self.click_count = 0
        return count

    def cleanup(self):
        GPIO.remove_event_detect(self.TEST_BUTTON_PIN)
        GPIO.cleanup()