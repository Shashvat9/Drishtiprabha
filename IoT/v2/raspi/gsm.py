import serial

# Serial Port Configuration
port = '/dev/ttyS0'  # Change if your serial port is different
baudrate = 9600

# SMS Details
phone_number = "+91XXXXXXXXXX"  # Replace with the recipient's phone number
message = "Hello from Raspberry Pi!"

try:
    ser = serial.Serial(port, baudrate, timeout=5)  # Open the serial port

    # Initialize SIM800L
    ser.write(b'AT+CMGF=1\r')  # Set SMS text mode
    ser.write(b'AT+CMGS="' + phone_number.encode() + b'"\r')
    ser.write(message.encode() + b"\r")  # Send the SMS content
    ser.write(bytes([26]))  # CTRL-Z to send the message
    
    print("SMS sent successfully!")
except serial.SerialException as e:
    print("Error:", e)
finally:
    ser.close()  # Close the serial port
