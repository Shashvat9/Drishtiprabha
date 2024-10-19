import RPi.GPIO as GPIO
import time

TRIG = 15 #3 in BCM mode
ECHO = 16 #4 in BCM mode

GPIO.setmode(GPIO.BOARD)
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

def measure_distance():
  pulse_start = None
  pulse_end = None

  GPIO.output(TRIG, False)
  time.sleep(0.28) # Adjust settling time if needed

  GPIO.output(TRIG, True)
  time.sleep(0.00005) # Adjust trigger pulse duration if needed
  GPIO.output(TRIG, False)
  
  
  while GPIO.input(ECHO) == 0:
    pulse_start = time.time()

  while GPIO.input(ECHO) == 1:
    pulse_end = time.time()
  #print("echo ",GPIO.input(ECHO))
  #print("start",pulse_start)
  #print("end",pulse_end)
  if pulse_start and pulse_end:
    pulse_duration = pulse_end - pulse_start
    distance = (pulse_duration * 34300) / 2  # Corrected calculation
    return round(distance, 2)
    #return(distance)
  else:
    return None # Indicate timeout or error

print("Waiting for sensor to settle")
#time.sleep(2) # Initial settling time

try:
  while True:
    distance = measure_distance()
    
    
    if distance is not None:
      if distance <= 200:
        print("Distance:", distance, "cm")
      else:
        continue
    else:
      print("Timeout waiting for echo pulse")

    #time.sleep(0.5) # Adjust delay between measurements

except KeyboardInterrupt:
  GPIO.cleanup()
  print("Exiting program...")

