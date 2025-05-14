from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langchain.tools import tool
from langgraph.prebuilt import create_react_agent
from dotenv import load_dotenv
import sys
from datetime import datetime
import requests
import os

# Load environment variables from .env file
load_dotenv()

# Get API key from environment variables
OPENWEATHER_API_KEY = os.getenv('OPENWEATHER_API_KEY')
if not OPENWEATHER_API_KEY:
    print("Warning: OPENWEATHER_API_KEY not found in environment variables.")

@tool
def calculator(operation: str, a: float, b: float) -> str:
    """Perform basic arithmetic calculations.
    
    Args:
        operation (str): The operation to perform ('add', 'subtract', 'multiply', 'divide')
        a (float): First number
        b (float): Second number
        
    Returns:
        str: The result of the calculation
    """
    try:
        print("Attempting to perform calculation...\n")

        if operation.lower() == 'add':
            result = a + b
            return f"The sum of {a} and {b} is {result}"
        elif operation.lower() == 'subtract':
            result = a - b
            return f"The difference between {a} and {b} is {result}"
        elif operation.lower() == 'multiply':
            result = a * b
            return f"The product of {a} and {b} is {result}"
        elif operation.lower() == 'divide':
            if b == 0:
                return "Error: Cannot divide by zero!"
            result = a / b
            return f"The quotient of {a} divided by {b} is {result}"
        else:
            return f"Error: Unknown operation '{operation}'. Please use 'add', 'subtract', 'multiply', or 'divide'."
    except Exception as e:
        return f"Error performing calculation: {str(e)}"

@tool
def get_weather(city: str) -> str:
    """Get current weather information for a city using OpenWeatherMap API.
    
    Args:
        city (str): The name of the city to get weather for
        
    Returns:
        str: Weather information for the city
    """
    if not OPENWEATHER_API_KEY:
        return "Error: OpenWeatherMap API key not found. Please set OPENWEATHER_API_KEY in your .env file."
    
    try:
        print("Attempting to get weather data...")
        # Make API request to OpenWeatherMap
        base_url = "http://api.openweathermap.org/data/2.5/weather"
        params = {
            'q': city,
            'appid': OPENWEATHER_API_KEY,
            'units': 'imperial'  # Use Fahrenheit for temperature
        }
        
        response = requests.get(base_url, params=params)
        
        if response.status_code == 200:
            data = response.json()

            print("\nAssistant: Grabbing the weather data...\n")
            
            # Extract relevant weather information
            temp = data['main']['temp']
            feels_like = data['main']['feels_like']
            humidity = data['main']['humidity']
            description = data['weather'][0]['description']
            wind_speed = data['wind']['speed']
            
            # Format the response
            current_time = datetime.now().strftime("%I:%M %p")
            return f"Current weather in {city} ({current_time}):\n" \
                   f"Temperature: {temp:.1f}°F (Feels like: {feels_like:.1f}°F)\n" \
                   f"Condition: {description.capitalize()}\n" \
                   f"Humidity: {humidity}%\n" \
                   f"Wind Speed: {wind_speed} mph"
        else:
            return f"Error: Weather API returned status code {response.status_code}. Please try again later."
               
    except requests.exceptions.ConnectionError:
        return "Error: Could not connect to the weather service. Please check your internet connection."
    except requests.exceptions.Timeout:
        return "Error: The weather service request timed out. Please try again."
    except requests.exceptions.RequestException as e:
        return f"Error fetching weather data: {str(e)}"
    except KeyError as e:
        return f"Error: Unexpected response format from weather service. Missing data: {str(e)}"
    except Exception as e:
        return f"An unexpected error occurred: {str(e)}"

def show_help():
    """Display available commands and tools."""
    print("\nAvailable Commands:")
    print("  help    - Show this help message")
    print("  quit    - Exit the program")
    print("\nAvailable Tools:")
    print("  Calculator: Can perform add, subtract, multiply, and divide operations")
    print("  Weather: Get current weather for major cities (New York, London, Tokyo, Sydney, Paris)")
    print("\nExample Usage:")
    print("  'Calculate 5 plus 3'")
    print("  'What's the weather in Tokyo?'")

def main():
    try:
        # Initialize the AI model
        model = ChatOpenAI(temperature=0)
        
        # Define available tools
        tools = [calculator, get_weather]
        
        # Create the agent
        agent_executor = create_react_agent(model, tools)

        user_name = input("\nAssistant: Hi! What is your name? ")
        
        print(f"\nAssistant: Welcome {user_name}! I'm your AI assistant. Type 'help' for available commands or 'quit' to exit.")
        
        while True:
            try:
                user_input = input("\nYou: ").strip()
                
                if user_input.lower() == "quit":
                    print(f"\nAssistant: Goodbye {user_name}! Have a great day!")
                    break
                elif user_input.lower() == "help":
                    show_help()
                    continue
                
                print("\nAssistant: ", end="")
                # Add system message to the input
                messages = [
                    SystemMessage(content="""You are a helpful AI assistant. When asked about weather, 
                    use the get_weather tool with the city name and return its output. For calculations,
                    use the calculator tool with the appropriate operation and numbers."""),
                    HumanMessage(content=user_input)
                ]
                
                for chunk in agent_executor.stream(
                    {"messages": messages}
                ):
                    if "agent" in chunk and "messages" in chunk["agent"]:
                        for message in chunk["agent"]["messages"]:
                            print(message.content, end="")
                
                print()
                
            except KeyboardInterrupt:
                print(f"\n\nAssistant: Goodbye {user_name}! Have a great day!\n")
                break
            except Exception as e:
                print(f"\nError: {str(e)}")
                print("Please try again or type 'help' for available commands.")
                
    except Exception as e:
        print(f"Fatal error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()

