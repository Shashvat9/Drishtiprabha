# import RPi.GPIO as GPIO
# import time

# class Ultrasonic:
#     def __init__(self, trig_pin=15, echo_pin=16):
#         self.TRIG = trig_pin
#         self.ECHO = echo_pin

#         # Board setup
#         GPIO.setmode(GPIO.BOARD)
#         GPIO.setup(self.TRIG, GPIO.OUT)
#         GPIO.setup(self.ECHO, GPIO.IN)

#         print("Waiting for sensor to settle")
#         time.sleep(0.5)  # Reduced settling time

#     def measure_distance(self):
#         GPIO.output(self.TRIG, False)
#         time.sleep(0.00001)

#         GPIO.output(self.TRIG, True)
#         time.sleep(0.00001)
#         GPIO.output(self.TRIG, False)

#         start_time = time.time()
#         timeout = start_time + 0.04  # 40ms timeout

#         while GPIO.input(self.ECHO) == 0 and start_time < timeout:
#             start_time = time.time()

#         if start_time >= timeout:
#             return 99999

#         end_time = time.time()
#         while GPIO.input(self.ECHO) == 1 and end_time < timeout:
#             end_time = time.time()

#         if end_time >= timeout:
#             return 99999

#         pulse_duration = end_time - start_time
#         distance = (pulse_duration * 34300) / 2
#         return round(distance, 2)

#     def cleanup(self):
#         GPIO.cleanup()
        
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

# ultrasonic.py (Migrated to gpiozero)

# Removed RPi.GPIO import
import time
# Import the specific gpiozero class needed
from gpiozero import DistanceSensor
from gpiozero.pins.lgpio import LGPIOFactory # Recommended factory for Pi 5
from gpiozero import Device

# Optional: Force lgpio pin factory (good for Pi 5)
# Device.pin_factory = LGPIOFactory()

class Ultrasonic:
    # Pin numbers should now be BCM
    # trig_pin: BOARD 15 -> BCM 22
    # echo_pin: BOARD 16 -> BCM 23
    def __init__(self, trig_pin=22, echo_pin=23):
        self.trig_pin = trig_pin
        self.echo_pin = echo_pin

        # Removed GPIO.setmode and GPIO.setup

        # Initialize DistanceSensor
        # max_distance=4 means ignore readings over 4 meters (adjust if needed)
        # threshold_distance for event handling (not used here, but available)
        try:
            self.sensor = DistanceSensor(
                echo=self.echo_pin,
                trigger=self.trig_pin,
                max_distance=4 # Default is 1m, increased here
            )
            print("Ultrasonic sensor initialized.")
            # No manual settling time needed usually, DistanceSensor handles it
        except Exception as e:
            print(f"Error initializing DistanceSensor (trig={self.trig_pin}, echo={self.echo_pin}): {e}")
            print("Ensure lgpio is installed ('pip install lgpio') and you have permissions (add user to gpio group).")
            # Optionally re-raise or handle differently
            raise


    def measure_distance(self):
        """Measures distance in centimeters."""
        # The DistanceSensor class handles the pulsing and timing.
        # '.distance' property returns distance in meters.
        try:
            # Read distance in meters and convert to cm
            distance_m = self.sensor.distance
            distance_cm = distance_m * 100

            # Handle potential edge case where sensor might return None briefly
            if distance_cm is None:
                return 99999 # Or another indicator for error/no reading

            # You might want to add checks for unrealistic values if needed
            # e.g., if distance_cm > self.sensor.max_distance * 100: return 99999

            return round(distance_cm, 2)

        except Exception as e:
             # Catch potential errors during read
             print(f"Error reading distance sensor: {e}")
             return 99999 # Indicate error


    def close(self):
        """Releases the GPIO resources used by the sensor."""
        print("Closing Ultrasonic sensor resources...")
        if hasattr(self, 'sensor'):
            self.sensor.close()
        # GPIO.cleanup() is handled globally by gpiozero or main script


# Example usage (optional, for testing this file directly)
if __name__ == "__main__":
    # Remember: trig 15 (BOARD) -> 22 (BCM), echo 16 (BOARD) -> 23 (BCM)
    ultrasonic_sensor = None
    try:
        ultrasonic_sensor = Ultrasonic(trig_pin=22, echo_pin=23)
        while True:
            distance = ultrasonic_sensor.measure_distance()
            # Handle the error code if returned
            if distance == 99999:
                print("Failed to get reading or sensor timeout.")
            else:
                print(f"Distance: {distance} cm")
            time.sleep(0.5) # Read every half second

    except KeyboardInterrupt:
        print("\nExiting")
    except Exception as e:
         print(f"An error occurred: {e}")
    finally:
        if ultrasonic_sensor:
            ultrasonic_sensor.close()