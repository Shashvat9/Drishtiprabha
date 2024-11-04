import RPi.GPIO as GPIO
import time

class Buzzer:
    def __init__(self, pin=37, duration=1):
        self.pin = pin
        self.duration = duration
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.pin, GPIO.OUT)
    
    def buzz(self):
        GPIO.output(self.pin, GPIO.HIGH)
        time.sleep(self.duration)
        GPIO.output(self.pin, GPIO.LOW)
    
    def cleanup(self):
        GPIO.cleanup()

if __name__ == "__main__":
    buzzer = Buzzer(pin=37, duration=1)
    
    try:
        while True:
            buzzer.buzz()
    except KeyboardInterrupt:
        buzzer.cleanup()
        
            
    # while True:
    #     buzzer.buzz()
        
    # # buzzer.cleanup()