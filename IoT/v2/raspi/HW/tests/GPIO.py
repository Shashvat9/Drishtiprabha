import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setup(15, GPIO.OUT)

while True:
    GPIO.output(15, GPIO.HIGH)
    print("GPIO pin 15 set to HIGH")
    time.sleep(1)
    
    GPIO.output(15, GPIO.LOW)
    print("GPIO pin 15 set to LOW")
    time.sleep(1)