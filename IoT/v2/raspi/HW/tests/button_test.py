import RPi.GPIO as GPIO 
import time

# Test setup
GPIO.setmode(GPIO.BOARD)

# Test button setup
TEST_BUTTON_PIN = 11  # Change to an available GPIO pin
GPIO.setup(TEST_BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

button_states = ["HOLD","double","triple"]

currunt_status = 0


def is_button_pressed():
    return GPIO.input(TEST_BUTTON_PIN) == GPIO.LOW

def button_released():
    return GPIO.input(TEST_BUTTON_PIN) == GPIO.HIGH

def button_click():
    # if button is pressed adn released in 0.5 seconds it will be button click
    
    if is_button_pressed():
        time.sleep(0.1)
        if button_released():
            return True
    return False

def button_click_count(timeout=1.5):
    click_count = 0
    start_time = time.time()

    while True:
        if is_button_pressed():
            # Wait for button release
            while is_button_pressed():
                time.sleep(0.05)
            click_count += 1
            time.sleep(0.1)  # Debounce
        if time.time() - start_time >= timeout:
            break
        time.sleep(0.05)
    return click_count

def press_and_hold():
    # if button is pressed for 2 seconds it will be press and hold
    
    start_time = time.time()
    while True:
        if is_button_pressed():
            if time.time() - start_time >= 2:
                return True
        else:
            start_time = time.time()
        time.sleep(0.1)
    return False
    
    
def detect_button_event():
    click_count = 0
    start_time = time.time()
    timeout = 1.5  # Time window to detect multiple clicks
    hold_time_threshold = 2  # Time threshold for press and hold

    while time.time() - start_time < timeout:
        if is_button_pressed():
            press_start = time.time()
            while is_button_pressed():
                time.sleep(0.05)
                if time.time() - press_start >= hold_time_threshold:
                    print("Button Press and Hold")
                    return "HOLD"
            click_count += 1
            time.sleep(0.1)  # Debounce
        time.sleep(0.05)

    if click_count == 1:
        print("Button Single Click")
        return "SINGLE"
    elif click_count == 2:
        print("Button Double Click")
        return "DOUBLE"
    elif click_count == 3:
        print("Button Triple Click")
        return "TRIPLE"
    else:
        print("No Button Click Detected")
        return "NONE"

def main():
    
    while True:
        # print("Button press count: ", button_click_count())
        # time.sleep(0.1)
        
        # if(button_click_count() == 1):
        #     print("Button clicked once")
        #     time.sleep(0.1)
        # elif(button_click_count() == 2):
        #     print("Button clicked twice")
        #     time.sleep(0.1)
        # elif(button_click_count() == 3):
        #     print("Button clicked thrice")
        #     time.sleep(0.1)
        # else:
        #     print("Button not clicked")
        #     time.sleep(0.1)
        
        print(detect_button_event())

if __name__ == "__main__":
    main()