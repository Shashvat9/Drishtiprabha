import socket
import geocoder      
      
      
def get_ip_address():
    hostname = socket.gethostname()
    IPAddr = socket.gethostbyname(hostname)
    return IPAddr
      
g = geocoder.ip(get_ip_address())  # Replace "my_ip_address" with your actual IP            
if g.ok:    
    
    print("Latitude:", g.lat)    
    print("Longitude:", g.lng)    
else:    
    print("Error getting location data")



