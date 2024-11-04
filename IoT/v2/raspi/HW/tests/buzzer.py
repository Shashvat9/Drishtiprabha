import RPi.GPIO as GPIO
import time

class BuzzerTest:
    def __init__(self, pin=37):
        self.pin = pin
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.pin, GPIO.OUT)
    
    def test_buzzer(self, duration=1):
        GPIO.output(self.pin, GPIO.HIGH)
        time.sleep(duration)
        GPIO.output(self.pin, GPIO.LOW)
    
    def cleanup(self):
        GPIO.cleanup()

if __name__ == "__main__":
    buzzer = BuzzerTest()
    buzzer.test_buzzer(duration=2)
    buzzer.cleanup()