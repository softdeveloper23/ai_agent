import os
from dotenv import load_dotenv
import requests

# Load environment variables
load_dotenv()

def test_weather_api():
    # Get API key
    api_key = os.getenv('OPENWEATHER_API_KEY')
    print(f"API Key found: {'Yes' if api_key else 'No'}")
    
    if not api_key:
        print("Error: No API key found in .env file")
        return
    
    # Test cities
    test_cities = ['Los Angeles', 'New York', 'London']
    
    for city in test_cities:
        print(f"\nTesting weather for {city}:")
        try:
            # Make API request
            base_url = "http://api.openweathermap.org/data/2.5/weather"
            params = {
                'q': city,
                'appid': api_key,
                'units': 'imperial'
            }
            
            print(f"Making request to {base_url}...")
            response = requests.get(base_url, params=params)
            print(f"Status code: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                temp = data['main']['temp']
                print(f"Success! Temperature in {city}: {temp}°F")
            else:
                print(f"Error response: {response.text}")
                
        except Exception as e:
            print(f"Error occurred: {str(e)}")

if __name__ == "__main__":
    test_weather_api() 