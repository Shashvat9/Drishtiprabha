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

    def set_frequency(self, frequency):
        self.frequency = frequency
        self.pwm.ChangeFrequency(self.frequency)

    def buzz_on(self, duration):
        self.pwm.ChangeDutyCycle(100)  # 100% duty cycle
        time.sleep(duration)
        self.buzz_off()

    def buzz_off(self):
        self.pwm.ChangeDutyCycle(0)    # 0% duty cycle to turn off

    def buzz_control(self, distance):
        # if distance <= 10:
        #     self.set_frequency(2000)
        #     self.buzz_on(0.05)
        # elif distance < 40:
        #     self.set_frequency(1500)
        #     self.buzz_on(0.15)
        # elif distance < 70:
        #     self.set_frequency(1000)
        #     self.buzz_on(0.25)
        # elif distance <= 100:
        #     self.set_frequency(500)
        #     self.buzz_on(0.35)
        # else:
        #     self.buzz_off()
        
        if(distance<=100 and distance>80):
            self.set_frequency(2000)
            self.buzz_on(distance/100)
        elif(distance<=80 and distance>50):
            self.set_frequency(1700)
            self.buzz_on(distance/800)
        elif(distance<=50):
            self.set_frequency(1500)
            self.buzz_on(distance/1000)

    def cleanup(self):
        self.pwm.stop()
        GPIO.cleanup()