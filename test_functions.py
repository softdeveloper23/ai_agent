import os
from dotenv import load_dotenv
import requests
from main import calculator, get_weather

# Load environment variables
load_dotenv()

def test_weather_api():
    print("\n=== Testing Weather API ===")
    # Get API key
    api_key = os.getenv('OPENWEATHER_API_KEY')
    print(f"API Key found: {'Yes' if api_key else 'No'}")
    
    if not api_key:
        print("Error: No API key found in .env file")
        return
    
    # Test cities
    test_cities = ['Los Angeles', 'New York', 'London', 'Tokyo', 'Paris']
    
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

def test_calculator():
    print("\n=== Testing Calculator Function ===")
    
    # Test cases for calculator
    test_cases = [
        ('add', 5, 3, 8),
        ('subtract', 10, 4, 6),
        ('multiply', 6, 7, 42),
        ('divide', 20, 5, 4),
        ('divide', 10, 0, None),  # Test division by zero
        ('invalid', 5, 3, None)   # Test invalid operation
    ]
    
    for operation, a, b, expected in test_cases:
        print(f"\nTesting {operation} with {a} and {b}:")
        try:
            # Use invoke method instead of direct call
            result = calculator.invoke({"operation": operation, "a": a, "b": b})
            print(f"Result: {result}")
            
            if expected is not None:
                # For valid operations, check if the result contains the expected number
                if str(expected) in result:
                    print("✓ Test passed")
                else:
                    print("✗ Test failed - unexpected result")
            else:
                # For invalid operations or division by zero, check if error message is present
                if "Error" in result:
                    print("✓ Test passed - error handled correctly")
                else:
                    print("✗ Test failed - error not handled correctly")
                    
        except Exception as e:
            print(f"✗ Test failed with error: {str(e)}")

def run_all_tests():
    print("Starting comprehensive tests...")
    test_weather_api()
    test_calculator()
    print("\nAll tests completed!")

if __name__ == "__main__":
    run_all_tests() 