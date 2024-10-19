import RPi.GPIO as GPIO
import time
import requests

#board setup
GPIO.setmode(GPIO.BOARD)

#ultrasonic setup
TRIG = 15 
ECHO = 16 
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

#buzzer setup
buzzer = 37
GPIO.setup(buzzer,GPIO.OUT)
Buzz = GPIO.PWM(buzzer, 1500) 

#button setup
BUTTON_PIN = 22
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

#api setup
def send_request(lon,let):
    params = {
        "api_key": "dp123",
        "longitude": lon,
        "latitude": let,
        "add": "dp1",
    }
    api_url = "https://drishtiprabha.000webhostapp.com/update_db.php"
    response = requests.get(api_url, params=params)  # Include parameters in URL

    # Check if the response is not empty
    if response.content:
        try:
            # Try to parse the response as JSON
            data = response.json()
            print(data)
        except ValueError:
            # The response couldn't be parsed as JSON, print the raw response
            print(response.text)
    else:
        print("Empty response")


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

def buzzer_methode(high):
	if high:
		Buzz.start(50)
	else:
		Buzz.start(0)
		
def buzz_control(distance):
	if distance<=100 and distance >=70:
		buzzer_methode(True)
		time.sleep(0.35)
		buzzer_methode(False)
	elif distance<70 and distance >=40:
		buzzer_methode(True)
		time.sleep(0.25)
		buzzer_methode(False)
	elif distance<40 and distance >=10:
		buzzer_methode(True)
		time.sleep(0.15)
		buzzer_methode(False)
	elif distance<10:
		buzzer_methode(True)
		
		
		

# main methode

def main():
  print("Waiting for sensor to settle")
  #time.sleep(2) # Initial settling time


  try:
    while True:
      distance = measure_distance()
      button_pressed = not GPIO.input(BUTTON_PIN)
      if button_pressed:
        time.sleep(5)
        buzzer_methode(True)
        send_request(72.820095,22.599911)
      else:
        if distance is not None:
          if distance <= 100:
            print("Distance:", distance, "cm")
            buzz_control(distance)
          else:
            continue
        else:
          print("Timeout waiting for echo pulse")

      #time.sleep(0.5) # Adjust delay between measurements

  except KeyboardInterrupt:
    GPIO.cleanup()
    print("Exiting program...")
    
  except requests.exceptions.RequestException as e:
      print(f"Error accessing API: {e}")
      
if __name__ == "__main__":
    main()
