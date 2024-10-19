import serial
import time
import RPi.GPIO as GPIO

# ---- Module Configuration ----

SERIAL_PORT = "/dev/serial0"  # Common serial port
BAUD_RATE = 9600

GPIO.setmode(GPIO.BOARD)  # Use BOARD pin numbering

# SIM800L Pin Connections (BOARD mode)
SIM800L_TXD = 10 
SIM800L_RXD = 8
SIM800L_RST = 36   

# ---- SIM800L Communication Functions ----

def send_at_command(command, timeout=1):
    ser.write((command + "\r\n").encode())
    time.sleep(timeout)
    response = ser.read(ser.inWaiting()).decode()
    return response

def initialize_sim800l():
    send_at_command("AT")      # Check module responsiveness
    send_at_command("ATE0")    # Disable echo
    send_at_command("AT+CMGF=1")  # Set SMS text mode

def send_sms(phone_number, message):
    send_at_command("AT+CMGS=\"" + phone_number + "\"")
    ser.write((message + "\x1A").encode())  # Ctrl+Z to send

# ---- Main Program ----

try:
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)

    # Initialize SIM800L module
    initialize_sim800l()

    phone_number = "+91XXXXXXXXXX"  # Replace with the recipient's number
    message = "Hello from Raspberry Pi!"

    # Send SMS
    send_sms(phone_number, message)

except Exception as e:
    print(f"An error occurred: {e}")
finally:
    if ser.isOpen():
        ser.close()
    GPIO.cleanup()
