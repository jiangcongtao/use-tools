import requests
import os
import json
from termcolor import colored
from datetime import datetime
from zoneinfo import ZoneInfo
from timezonefinder import TimezoneFinder

def clean_input(input_str):
    """
    Clean the input string by replacing single quotes with double quotes
    and removing any extraneous characters such as trailing quotes.

    Parameters:
    input_str (str): The input string to be cleaned.

    Returns:
    str: The cleaned input string.
    """
    # print('input_str:', input_str)
    if isinstance(input_str, dict) is False:
        input_str_clean = input_str.replace("'", "\"")
        input_str_clean = input_str_clean.strip().strip("\"")
        # print('input_str_clean:', input_str)
        if 'city_name' in input_str:
            return json.loads(input_str_clean)
        else:
            return {'city_name': input_str}
  
    return input_str

def get_weather_data_from_remote(city_name):
    """
    Retrieve weather data from the OpenWeatherMap API for the specified city.

    Parameters:
    city_name (str): The name of the city for which the weather data will be retrieved.

    Returns:
    requests.Response: The response object containing the weather data.
    """
    api_key = os.environ.get('WEATHER_API_KEY')
    base_url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}"
    response = requests.get(base_url)
    # print("base_url:", base_url)

    return response

def get_current_weather(city_name):
    """
    Get the current weather of the specified city.

    Parameters:
    city_name (str): The name of the city for which the current weather will be retrieved.

    Returns:
    str: The current weather of the specified city.
    """
    param = clean_input(city_name)
    response = get_weather_data_from_remote(param['city_name'])

    if response.status_code == 200:
        weather_data = response.json()
        city = weather_data["name"]
        country = weather_data["sys"]["country"]
        description = weather_data["weather"][0]["description"]
        temperature = weather_data["main"]["temp"] - 273.15  # Convert Kelvin to Celsius

        print('Executed using get_current_weather function')
        return f"Current weather in {city} [{country}]: {description}\nTemperature: {temperature:.2f} °C"
    else:
        print(colored(f"Error: {response.status_code}", 'red'))
        os.abort()

def get_local_time(city_name):
    """
    Get the current or local time of the specified city.

    Parameters:
    city_name (str): The name of the city for which the current or local time will be retrieved.

    Returns:
    str: The current or local time of the specified city.
    """
    param = clean_input(city_name)
    response = get_weather_data_from_remote(param['city_name'])

    if response.status_code == 200:
        weather_data = response.json()
        city = weather_data["name"]
        country = weather_data["sys"]["country"]
        lon = weather_data["coord"]["lon"]
        lat = weather_data["coord"]["lat"]

        tf = TimezoneFinder()
        timezone_str = tf.timezone_at(lng=lon, lat=lat)

        if timezone_str is None:
            return f"Could not determine timezone for {city}"

        timezone = ZoneInfo(timezone_str)
        local_time = datetime.now(timezone)
        local_time_str = local_time.strftime("%Y-%m-%d %H:%M:%S %Z")
        print('Executed using get_local_time function')

        return f"Current local time in {city} [{country}]\nLocal Time: {local_time_str}"
    else:
        print(colored(f"Error: {response.status_code}", 'red'))
        os.abort()
