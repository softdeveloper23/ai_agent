from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langchain.tools import tool
from langgraph.prebuilt import create_react_agent
from dotenv import load_dotenv
import sys
from datetime import datetime

# Load environment variables from .env file
load_dotenv()

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
    """Get current weather information for a city.
    
    Args:
        city (str): The name of the city to get weather for
        
    Returns:
        str: Weather information for the city
    """
    # This is a mock implementation - in a real app, you would call a weather API
    current_time = datetime.now().strftime("%I:%M %p")
    weather_data = {
        "New York": {"temp": 72, "condition": "sunny", "humidity": 65},
        "London": {"temp": 60, "condition": "cloudy", "humidity": 80},
        "Tokyo": {"temp": 75, "condition": "clear", "humidity": 70},
        "Sydney": {"temp": 68, "condition": "partly cloudy", "humidity": 75},
        "Paris": {"temp": 65, "condition": "rainy", "humidity": 85}
    }
    
    if city not in weather_data:
        return f"Sorry, I don't have weather data for {city}. Try one of these cities: {', '.join(weather_data.keys())}"
    
    data = weather_data[city]
    return f"Current weather in {city} ({current_time}):\n" \
           f"Temperature: {data['temp']}°F\n" \
           f"Condition: {data['condition']}\n" \
           f"Humidity: {data['humidity']}%"

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
        
        print("Welcome! I'm your AI assistant. Type 'help' for available commands or 'quit' to exit.")
        
        while True:
            try:
                user_input = input("\nYou: ").strip()
                
                if user_input.lower() == "quit":
                    print("\nAI: Goodbye! Have a great day!")
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
                print("\n\nAI: Goodbye! Have a great day!")
                break
            except Exception as e:
                print(f"\nError: {str(e)}")
                print("Please try again or type 'help' for available commands.")
                
    except Exception as e:
        print(f"Fatal error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()

