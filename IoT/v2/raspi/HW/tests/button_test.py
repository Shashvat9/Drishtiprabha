import RPi.GPIO as GPIO 
import time

# Test setup
GPIO.setmode(GPIO.BOARD)

# Test button setup
TEST_BUTTON_PIN = 11  # Change to an available GPIO pin
GPIO.setup(TEST_BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

button_states = ["HOLD","double","triple"]

currunt_status = 0

button_click_count = 0

def is_button_pressed():
    return GPIO.input(TEST_BUTTON_PIN) == GPIO.LOW

def button_released():
    return GPIO.input(TEST_BUTTON_PIN) == GPIO.HIGH

def button_click():
    # if button is pressed adn released in 0.5 seconds it will be button click
    
    if is_button_pressed():
        time.sleep(0.2)
        if button_released():
            return True
    return False

def button_press_count():
    global button_click_count
    if button_click():
        button_click_count += 1
        while is_button_pressed():
            time.sleep(0.1)
    if button_click_count == 2:
        print("Button double clicked")
        button_click_count = 0
        return "double"
    elif button_click_count == 3:
        print("Button triple clicked")
        button_click_count = 0
        return "triple"
    return button_click_count


# def button_press_count():
#     press_count = 0
#     last_press_time = None
#     while press_count < 3:
#         if is_button_pressed():
#             if last_press_time is None or time.time() - last_press_time > 0.5:
#                 press_count += 1
#                 last_press_time = time.time()
#                 while is_button_pressed():
#                     time.sleep(0.1)  # Wait for button release
#         time.sleep(0.1)
#     return press_count

# def press_and_hold_5_seconds():
#     start_time = None
#     while True:
#         if GPIO.input(TEST_BUTTON_PIN) == GPIO.LOW:
#             if start_time is None:
#                 start_time = time.time()
#             elif time.time() - start_time >= 5:
#                 # print("Button pressed and held for 5 seconds!")
#                 return True
#         else:
#             start_time = None
#         time.sleep(0.1)
#     return False

# def double_press():
#     press_count = 0
#     last_press_time = None
#     while press_count < 2:
#         if GPIO.input(TEST_BUTTON_PIN) == GPIO.LOW:
#             if last_press_time is None or time.time() - last_press_time > 0.5:
#                 press_count += 1
#                 last_press_time = time.time()
#                 while GPIO.input(TEST_BUTTON_PIN) == GPIO.LOW:
#                     time.sleep(0.1)  # Wait for button release
#         time.sleep(0.1)
#     if press_count == 2:
#         # print("Button double pressed!")
#         return True
#     return False

# def triple_press():
#     press_count = 0
#     last_press_time = None
#     while press_count < 3:
#         if GPIO.input(TEST_BUTTON_PIN) == GPIO.LOW:
#             if last_press_time is None or time.time() - last_press_time > 0.5:
#                 press_count += 1
#                 last_press_time = time.time()
#                 while GPIO.input(TEST_BUTTON_PIN) == GPIO.LOW:
#                     time.sleep(0.1)  # Wait for button release
#         time.sleep(0.1)
#     if press_count == 3:
#         # print("Button triple pressed!")
#         return True
#     return False

def main():
    # try:
    #     while True:
    #         if press_and_hold_5_seconds():
    #             print("Detected: Press and hold for 5 seconds")
    #         elif double_press():
    #             print("Detected: Double press")
    #         elif triple_press():
    #             print("Detected: Triple press")
    #         time.sleep(1)  # Delay before next detection cycle
    # except KeyboardInterrupt:
    #     pass
    # finally:
    #     GPIO.cleanup()
    # while True:
        # if(is_button_pressed()):
        #     print("Button pressed")
        #     time.sleep(0.1)
        # elif(button_released()):
        #     print("Button released")
        #     time.sleep(0.1)
        # else:
        #     print("Button not pressed")
        #     time.sleep(0.1)
        
        # if(button_click()):
        #     print("Button clicked")
        #     time.sleep(0.1)
        # else:
        #     print("Button not clicked")
        #     time.sleep(0.1)
        
    # print("Press count: ", button_press_count())
    while True:
        print("Button press count: ", button_press_count())
        time.sleep(0.1)

if __name__ == "__main__":
    main()