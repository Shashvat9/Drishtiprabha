import serial
import time
import RPi.GPIO as GPIO

# GPS Module Configuration
GPS_SERIAL_PORT = "/dev/ttyAMA0"  # Common serial port for GPS
GPS_BAUD_RATE = 9600

# Initialize GPIO
GPIO.setmode(GPIO.BOARD)

def parse_nmea_sentence(sentence):
    parts = sentence.split(',')
    if parts[0] == "$GPGGA":
        try:
            lat = parts[2]
            lat_dir = parts[3]
            lon = parts[4]
            lon_dir = parts[5]
            if lat and lon:
                lat = float(lat[:2]) + float(lat[2:]) / 60.0
                lon = float(lon[:3]) + float(lon[3:]) / 60.0
                if lat_dir == 'S':
                    lat = -lat
                if lon_dir == 'W':
                    lon = -lon
                print(f"Latitude: {lat} {lat_dir}, Longitude: {lon} {lon_dir}")
            else:
                print("No GPS fix")
        except ValueError:
            print("Error parsing NMEA sentence")
    else:
        print("Unsupported NMEA sentence")

def initialize_gps():
    try:
        ser = serial.Serial(GPS_SERIAL_PORT, GPS_BAUD_RATE, timeout=1)
        ser.flush()
        return ser
    except Exception as e:
        print(f"Failed to initialize GPS: {e}")
        return None

def read_gps_data(ser):
    if ser and ser.isOpen():
        try:
            line = ser.readline().decode('ascii', errors='ignore').strip()
            if line.startswith('$'):
                parse_nmea_sentence(line)
        except Exception as e:
            print(f"Error reading GPS data: {e}")
    else:
        print("Serial port not open")

def main():
    ser = initialize_gps()
    if ser:
        try:
            while True:
                read_gps_data(ser)
                time.sleep(1)  # Adjust delay as needed
        except KeyboardInterrupt:
            print("Terminating GPS test")
        finally:
            if ser.isOpen():
                ser.close()
            GPIO.cleanup()
    else:
        print("Failed to initialize GPS module")

if __name__ == "__main__":
    main()