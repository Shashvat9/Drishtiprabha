import subprocess
import requests
import json

def get_wifi_access_points():
    try:
        # Execute the system command to scan Wi-Fi networks
        scan_output = subprocess.check_output(['netsh', 'wlan', 'show', 'networks', 'mode=Bssid'], universal_newlines=True)
        
        # Regular expressions to extract SSID, BSSID, and Signal Strength
        ssid_re = re.compile(r"SSID \d+ : (.+)")
        bssid_re = re.compile(r"BSSID \d+ : ([\w:]+)")
        signal_re = re.compile(r"Signal\s*:\s*(\d+)%")
        
        wifi_access_points = []
        current_ap = {}
        for line in scan_output.split('\n'):
            ssid_match = ssid_re.search(line)
            if ssid_match:
                current_ap = {}
                current_ap['ssid'] = ssid_match.group(1).strip()
                continue
            bssid_match = bssid_re.search(line)
            if bssid_match and current_ap:
                current_ap['macAddress'] = bssid_match.group(1)
                continue
            signal_match = signal_re.search(line)
            if signal_match and 'macAddress' in current_ap:
                current_ap['signalStrength'] = int(signal_match.group(1))
                current_ap['signalToNoiseRatio'] = 0  # Not directly available
                wifi_access_points.append(current_ap)
        return wifi_access_points
    except subprocess.CalledProcessError as e:
        print(f"Failed to scan Wi-Fi access points: {e}")
        return []

def get_location(api_key):
    wifi_access_points = get_wifi_access_points()
    if not wifi_access_points:
        return None

    # Prepare the request payload
    payload = {
        "wifiAccessPoints": wifi_access_points
    }

    # Send the request to Google Geolocation API
    response = requests.post(
        'https://www.googleapis.com/geolocation/v1/geolocate?key=' + api_key,
        data=json.dumps(payload),
        headers={'Content-Type': 'application/json'}
    )

    # Parse the response
    if response.status_code == 200:
        location = response.json().get('location', {})
        return location.get('lat'), location.get('lng')
    else:
        print(f"API request failed with status code: {response.status_code}")
        print(f"Response: {response.text}")
        return None

# Example usage
api_key = 'AIzaSyC-iSJulKT-gdv4JF3_hc3UZfYlRWWh6w4'
location = get_location(api_key)
if location:
    latitude, longitude = location
    print(f"Latitude: {latitude}, Longitude: {longitude}")
    maps_url = f"https://www.google.com/maps/search/?api=1&query={latitude},{longitude}"
    print(f"Google Maps URL: {maps_url}")
else:
    print("Could not determine location")