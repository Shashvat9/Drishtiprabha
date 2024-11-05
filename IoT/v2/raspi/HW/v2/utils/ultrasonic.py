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
        time.sleep(0.5)  # Reduced settling time

    def measure_distance(self):
        GPIO.output(self.TRIG, False)
        time.sleep(0.00001)

        GPIO.output(self.TRIG, True)
        time.sleep(0.00001)
        GPIO.output(self.TRIG, False)

        start_time = time.time()
        timeout = start_time + 0.04  # 40ms timeout

        while GPIO.input(self.ECHO) == 0 and start_time < timeout:
            start_time = time.time()

        if start_time >= timeout:
            return 99999

        end_time = time.time()
        while GPIO.input(self.ECHO) == 1 and end_time < timeout:
            end_time = time.time()

        if end_time >= timeout:
            return 99999

        pulse_duration = end_time - start_time
        distance = (pulse_duration * 34300) / 2
        return round(distance, 2)

    def cleanup(self):
        GPIO.cleanup()
        
# if __name__ == "__main__":
#     ultrasonic_sensor = Ultrasonic(trig_pin=15, echo_pin=16)
#     try:
#         while True:
#             distance = ultrasonic_sensor.measure_distance()
#             print(f"Distance: {distance} cm")
#             # time.sleep(1)
#     except KeyboardInterrupt:
#         ultrasonic_sensor.cleanup()
#         print("Exiting")