import requests
import os
from termcolor import colored

def get_current_weather(city_name):
    """
    Get the current weather of the specified city_name.

    Parameters:
    city_name (str): The name of the city for which the current weather will be retrived.

    Returns:
    str: The current weather of the specified city.
    """

    api_key = os.environ.get('WEATHER_API_KEY')
    # Base URL for the API call
    base_url = (
        f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}"
    )

    # Send GET request to retrieve weather data
    response = requests.get(base_url)

    # Check for successful response
    if response.status_code == 200:
        # Parse JSON data
        weather_data = response.json()

        # Extract relevant information
        city = weather_data["name"]
        country = weather_data["sys"]["country"]
        description = weather_data["weather"][0]["description"]
        temperature = weather_data["main"]["temp"] - 273.15  # Convert Kelvin to Celsius

        print('Executed using get_current_weather function')

        return f"Current weather in {city} [{country}]: {description}\nTemperature: {temperature:.2f} °C"
    else:
        print(colored(f"Error: {response.status_code}",'red'))
        os.abort()

