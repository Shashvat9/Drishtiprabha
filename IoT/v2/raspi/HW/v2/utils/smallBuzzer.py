import RPi.GPIO as GPIO
import time

class BuzzerSmall:
    def __init__(self, pin=37, frequency=1000):
        self.pin = pin
        # self.duration = duration
        self.frequency = frequency  # Frequency in Hertz
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.pin, GPIO.OUT)
        self.pwm = GPIO.PWM(self.pin, self.frequency)

    def buzz(self,duration):
        self.pwm.start(50)  # Start PWM with 50% duty cycle
        time.sleep(duration)
        self.pwm.stop()

    def buzz_control(self, distance):
        """Controls the buzzer based on distance with fixed frequency."""
        duration = 0

        if 80 < distance < 90:
            # Frequency is fixed, only adjust duration
            duration = distance / 500
        elif 50 < distance <= 80:
            # Frequency is fixed, only adjust duration
            duration = distance / 800
        elif distance <= 50:
            # Frequency is fixed, only adjust duration
            duration = distance / 1000

        if duration > 0:
            self.buzz(1)
        # No else needed, if distance is >= 90, nothing happens

    def beep_long(self):
        """Produces a long beep at the fixed frequency."""
        # Frequency is fixed
        self.buzz(1) # 1 second duration

    def beep_short(self):
        """Produces a short beep at the fixed frequency."""
        # Frequency is fixed
        self.buzz(0.5) # 0.5 second duration

    def beep_request_ec2(self):
        """Produces a beep indicating an EC2 request at the fixed frequency."""
        # Frequency is fixed
        self.buzz(2) # 2 second duration

    def cleanup(self):
        """Stops the PWM and cleans up GPIO resources."""
        self.pwm.stop()
        # Consider letting the main script handle GPIO.cleanup()
        # GPIO.cleanup(self.pin) # Clean up only the pin used by this instance
