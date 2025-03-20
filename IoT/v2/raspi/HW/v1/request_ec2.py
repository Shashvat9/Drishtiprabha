import requests

class EC2Request:
    def __init__(self, api_key, longitude, latitude, d_id):
        self.api_key = api_key
        self.longitude = longitude
        self.latitude = latitude
        self.d_id = d_id
        self.api_url = "http://13.202.118.172/api/v2/update_db.php"

    def send_request(self):
        params = {
            "api_key": self.api_key,
            "longitude": self.longitude,
            "latitude": self.latitude,
            "d_id": self.d_id,
        }
        try:
            response = requests.get(self.api_url, params=params)
            response.raise_for_status()  # Raise an exception for HTTP errors
            data = response.json()
            print(data)
        except requests.exceptions.RequestException as e:
            print(f"Error accessing API: {e}")
        except ValueError:
            print("Error parsing JSON response")

if __name__ == "__main__":
    ec2_request = EC2Request(api_key="dp123", longitude=72.820095, latitude=22.599911, d_id="2")
    ec2_request.send_request()