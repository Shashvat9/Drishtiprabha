import RPi.GPIO as GPIO
import time

class Buzzer:
    def __init__(self, pin=37, duration=1, frequency=1000):
        self.pin = pin
        self.duration = duration
        self.frequency = frequency  # Frequency in Hertz
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.pin, GPIO.OUT)
        self.pwm = GPIO.PWM(self.pin, self.frequency)

    def buzz(self):
        self.pwm.start(50)  # Start PWM with 50% duty cycle
        time.sleep(self.duration)
        self.pwm.stop()

    def cleanup(self):
        GPIO.cleanup()

if __name__ == "__main__":
    buzzer = Buzzer(pin=37, duration=1, frequency=1000)
    try:
        while True:
            buzzer.buzz()
            time.sleep(1)
    except KeyboardInterrupt:
        buzzer.cleanup()