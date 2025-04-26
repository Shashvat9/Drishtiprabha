# import RPi.GPIO as GPIO
# import time

# class Buzzer:
#     def __init__(self, pin=37, frequency=1500):
#         self.pin = pin
#         self.frequency = frequency
#         GPIO.setmode(GPIO.BOARD)
#         GPIO.setup(self.pin, GPIO.OUT)
#         self.pwm = GPIO.PWM(self.pin, self.frequency)
#         self.pwm.start(0)  # Start with buzzer off

#     def set_frequency(self, frequency):
#         self.frequency = frequency
#         self.pwm.ChangeFrequency(self.frequency)

#     def buzz_on(self, duration):
#         self.pwm.ChangeDutyCycle(100)  # 100% duty cycle
#         time.sleep(duration)
#         self.buzz_off()

#     def buzz_off(self):
#         self.pwm.ChangeDutyCycle(0)    # 0% duty cycle to turn off

#     def buzz_control(self, distance):
#         if(distance<90 and distance>80):
#             self.set_frequency(1500)
#             self.buzz_on(distance/500)
#         elif(distance<=80 and distance>50):
#             self.set_frequency(1700)
#             self.buzz_on(distance/800)
#         elif(distance<=50):
#             self.set_frequency(2000)
#             self.buzz_on(distance/1000)
            
#     def beep_long(self):
#         self.set_frequency(2000)
#         self.buzz_on(1)
        
#     def beep_short(self):
#         self.set_frequency(2000)
#         self.buzz_on(0.5)
        
#     def beep_request_ec2(self):
#         self.set_frequency(2000)
#         self.buzz_on(2)
    
#     def cleanup(self):
#         self.pwm.stop()
#         GPIO.cleanup()

# buzzer.py (Migrated to gpiozero)

# Removed RPi.GPIO import
import time
# Import the specific gpiozero class needed
from gpiozero import PWMOutputDevice
from gpiozero.pins.lgpio import LGPIOFactory # Recommended factory for Pi 5
from gpiozero import Device

# Optional: Force lgpio pin factory (good for Pi 5)
# Device.pin_factory = LGPIOFactory()

class Buzzer:
    # Pin number should now be BCM (BOARD 37 -> BCM 26)
    def __init__(self, pin=26, frequency=1500):
        self.pin = pin
        self.frequency = frequency
        # Removed GPIO.setmode and GPIO.setup

        # Initialize PWMOutputDevice
        # initial_value=0 means start with buzzer off (0% duty cycle)
        try:
            self.pwm_device = PWMOutputDevice(
                self.pin,
                frequency=self.frequency,
                initial_value=0
            )
        except Exception as e:
            print(f"Error initializing PWMOutputDevice on pin {self.pin}: {e}")
            print("Ensure lgpio is installed ('pip install lgpio') and you have permissions (add user to gpio group).")
            # Optionally re-raise or handle differently
            raise

    def set_frequency(self, frequency):
        if frequency > 0: # Avoid invalid frequency
            self.frequency = frequency
            self.pwm_device.frequency = self.frequency
        else:
            print(f"Warning: Invalid frequency {frequency} requested.")


    def buzz_on(self, duration):
        if duration > 0:
            # Use pwm_device.value (0.0 to 1.0) instead of ChangeDutyCycle
            self.pwm_device.value = 1.0  # 100% duty cycle
            time.sleep(duration)
            self.buzz_off()
        else:
             self.buzz_off()

    def buzz_off(self):
        self.pwm_device.value = 0.0  # 0% duty cycle to turn off

    def buzz_control(self, distance):
        # Keep distance logic, but ensure buzz_on handles duration=0 edge case
        buzz_duration = 0
        new_frequency = 0

        if 80 < distance < 90 :
            new_frequency = 1500
            buzz_duration = distance / 500
        elif 50 < distance <= 80:
            new_frequency = 1700
            buzz_duration = distance / 800
        elif distance <= 50:
            new_frequency = 2000
            buzz_duration = distance / 1000

        if buzz_duration > 0:
            self.set_frequency(new_frequency)
            self.buzz_on(buzz_duration)
        else:
            # Ensure buzzer is off if not in range or duration is zero
            self.buzz_off()


    def beep_long(self):
        self.set_frequency(2000)
        self.buzz_on(1)

    def beep_short(self):
        self.set_frequency(2000)
        self.buzz_on(0.5)

    def beep_request_ec2(self):
        self.set_frequency(2000)
        self.buzz_on(2)

    def close(self):
        """Releases the GPIO resources used by the buzzer."""
        print("Closing Buzzer resources...")
        # pwm.stop() is replaced by pwm_device.close()
        if hasattr(self, 'pwm_device'):
             self.pwm_device.close()
        # GPIO.cleanup() is handled globally by gpiozero or main script


# Example usage (optional, for testing this file directly)
if __name__ == "__main__":
    test_buzzer = None
    try:
        # Remember: pin 37 (BOARD) is pin 26 (BCM)
        test_buzzer = Buzzer(pin=26)
        print("Testing short beep...")
        test_buzzer.beep_short()
        time.sleep(1)
        print("Testing long beep...")
        test_buzzer.beep_long()
        time.sleep(1)
        print("Testing distance control (simulated)...")
        test_buzzer.buzz_control(85) # Should beep briefly
        time.sleep(0.5)
        test_buzzer.buzz_control(60) # Should beep briefly
        time.sleep(0.5)
        test_buzzer.buzz_control(40) # Should beep briefly
        time.sleep(0.5)
        test_buzzer.buzz_control(100) # Should be silent
        print("Test finished.")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if test_buzzer:
            test_buzzer.close()