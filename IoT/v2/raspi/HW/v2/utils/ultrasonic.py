import RPi.GPIO as GPIO
import time

class Ultrasonic:
    def __init__(self, trig_pin=15, echo_pin=16):
        self.TRIG = trig_pin
        self.ECHO = echo_pin

        # Board setup
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.TRIG, GPIO.OUT)
        GPIO.setup(self.ECHO, GPIO.IN)

        print("Waiting for sensor to settle")
        time.sleep(2)  # Initial settling time

    def measure_distance(self):
        pulse_start = None
        pulse_end = None

        GPIO.output(self.TRIG, False)
        time.sleep(0.005)

        GPIO.output(self.TRIG, True)
        time.sleep(0.00005)
        GPIO.output(self.TRIG, False)

        while GPIO.input(self.ECHO) == 0:
            pulse_start = time.time()

        while GPIO.input(self.ECHO) == 1:
            pulse_end = time.time()

        if pulse_start and pulse_end:
            pulse_duration = pulse_end - pulse_start
            distance = (pulse_duration * 34300) / 2  # Corrected calculation
            return round(distance, 2)
        else:
            return "Error"

    def cleanup(self):
        GPIO.cleanup()
        
# if __name__ == "__main__":
#     ultrasonic_sensor = Ultrasonic()
#     try:
#         while True:
#             distance = ultrasonic_sensor.measure_distance()
#             print(f"Distance: {distance} cm")
#             time.sleep(1)
#     except KeyboardInterrupt:
#         ultrasonic_sensor.cleanup()