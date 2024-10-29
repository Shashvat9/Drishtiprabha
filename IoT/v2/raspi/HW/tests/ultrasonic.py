import RPi.GPIO as GPIO 
import time

#board setup
GPIO.setmode(GPIO.BOARD)

#ultrasonic setup
TRIG = 15 
ECHO = 16 
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)


def measure_distance():
  pulse_start = None
  pulse_end = None

  GPIO.output(TRIG, False)
  #time.sleep(0.28) # Adjust settling time if needed
  time.sleep(0.005)

  GPIO.output(TRIG, True)
  time.sleep(0.00005) # Adjust trigger pulse duration if needed
  GPIO.output(TRIG, False)
  
  
  while GPIO.input(ECHO) == 0:
    pulse_start = time.time()

  while GPIO.input(ECHO) == 1:
    pulse_end = time.time()
  if pulse_start and pulse_end:
    pulse_duration = pulse_end - pulse_start
    distance = (pulse_duration * 34300) / 2  # Corrected calculation
    return round(distance, 2)
  else:
    return None # Indicate timeout or error
  
  
def main():
  print("Waiting for sensor to settle")
  time.sleep(2) # Initial settling time


  try:
    while True:
      print("Measuring distance")
      distance = measure_distance()
      print(f"Distance: {distance} cm")

      time.sleep(0.5) # Adjust delay between measurements

  except KeyboardInterrupt:
    GPIO.cleanup()
    print("Exiting program...")
    
  except requests.exceptions.RequestException as e:
      print(f"Error accessing API: {e}")
      

if __name__ == "__main__":
  main()