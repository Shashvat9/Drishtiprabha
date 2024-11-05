import RPi.GPIO as GPIO
import time
import threading

class ButtonHandler:
    def __init__(self, pin=11, debounce_time=0.05, click_time=0.3, hold_time=2):
        """
        Initializes the ButtonHandler.

        :param pin: GPIO pin number where the button is connected.
        :param debounce_time: Time to debounce button presses (in seconds).
        :param click_time: Maximum interval between clicks to be considered part of the same sequence.
        :param hold_time: Duration to consider a press as a long hold (in seconds).
        """
        GPIO.setmode(GPIO.BOARD)
        self.button_pin = pin
        GPIO.setup(self.button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        self.debounce_time = debounce_time
        self.click_time = click_time
        self.hold_time = hold_time

        self.click_count = 0
        self.last_click_time = 0
        self.hold_detected = False
        self.lock = threading.Lock()
        self.hold_timer = None

        GPIO.add_event_detect(self.button_pin, GPIO.BOTH, callback=self._handle_event, bouncetime=int(self.debounce_time * 1000))

    def _handle_event(self, channel):
        """
        Internal callback to handle button events.
        """
        if GPIO.input(self.button_pin) == GPIO.LOW:
            # Button pressed
            self.press_time = time.time()
            if self.hold_timer is None:
                self.hold_timer = threading.Timer(self.hold_time, self._detect_hold)
                self.hold_timer.start()
        else:
            # Button released
            release_time = time.time()
            press_duration = release_time - self.press_time

            if self.hold_timer is not None:
                self.hold_timer.cancel()
                self.hold_timer = None

            if press_duration >= self.hold_time:
                # Long press detected
                with self.lock:
                    self.click_count = 5  # Special value for hold
                self.hold_detected = True
            else:
                # Short press detected
                current_time = time.time()
                with self.lock:
                    if (current_time - self.last_click_time) > self.click_time:
                        self.click_count = 1
                    else:
                        self.click_count += 1
                self.last_click_time = current_time

    def _detect_hold(self):
        """
        Callback for detecting a long press.
        """
        with self.lock:
            self.click_count = 5  # Special value for hold
            self.hold_detected = True

    def get_click_count(self):
        """
        Retrieves and resets the current click count.

        :return: Number of clicks detected or 5 for a hold.
        """
        with self.lock:
            count = self.click_count
            self.click_count = 0
        return count

    def cleanup(self):
        """
        Cleans up GPIO settings.
        """
        GPIO.remove_event_detect(self.button_pin)
        GPIO.cleanup()