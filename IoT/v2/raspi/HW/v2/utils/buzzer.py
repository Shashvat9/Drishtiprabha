import RPi.GPIO as GPIO
import time

class Buzzer:
    def __init__(self, pin=37, frequency=1500):
        self.pin = pin
        self.frequency = frequency
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.pin, GPIO.OUT)
        self.pwm = GPIO.PWM(self.pin, self.frequency)
        self.pwm.start(0)  # Start with buzzer off

    def buzz_on(self):
        self.pwm.ChangeDutyCycle(100)  # 100% duty cycle

    def buzz_off(self):
        self.pwm.ChangeDutyCycle(0)    # 0% duty cycle to turn off

    def buzz_control(self, distance):
        # if 70 <= distance <= 100:
        #     self.buzz_on()
        #     time.sleep(0.35)
        #     self.buzz_off()
        # elif 40 <= distance < 70:
        #     self.buzz_on()
        #     time.sleep(0.25)
        #     self.buzz_off()
        # elif 10 <= distance < 40:
        #     self.buzz_on()
        #     time.sleep(0.15)
        #     self.buzz_off()
        # elif distance < 10:
        #     self.buzz_on()
        # else:
        #     self.buzz_off()
        self.buzz_on()
        time.sleep(distance/100)
        self.buzz_off()

    def cleanup(self):
        self.pwm.stop()
        GPIO.cleanup()