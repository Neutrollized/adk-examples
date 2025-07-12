"""This module provides tools for weather and time related information."""
import requests
import json
from datetime import datetime


#-------------------
# settings
#-------------------
# SSL verification for requests
verify=True


#-------------------
# function tools
#-------------------
def get_geocoding(city: str, country: str) -> dict:
    """Find geographical location given city and country
    Args:
        city: A string representing the name of the city.
        country: A string representing the name or country code of the country.

    Returns:
        dict: Latitude and longitude of the city, country.
    """
    url = "https://geocoding-api.open-meteo.com/v1/search"

    query=f"{url}?name={city}"
    try:
        response = requests.get(query, verify=verify)
    except requests.exceptions.Timeout as e:
        print(f"Timeout error: {e}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None
    json_data = json.loads(response.text)

    try:
        for entry in json_data["results"]:
            try:
                if entry["country"].lower() == country.lower():
                    return {"latitude": entry["latitude"], "longitude": entry["longitude"]}
            except KeyError:
                return None
    except KeyError:
        return None


def find_current_weather(latitude: float, longitude: float) -> float:
    """Find weather given geographical location
    Args:
        latitude: A float representing the latitude of a geographical location.
        longitude: A float representing the longitude of a geographical location.

    Returns:
        float: Current temperature in Celcius
    """
    url = "https://api.open-meteo.com/v1/forecast"

    query=f"{url}?latitude={latitude}&longitude={longitude}&current=temperature_2m"
    try:
        response = requests.get(query, verify=verify)
    except requests.exceptions.Timeout as e:
        print(f"Timeout error: {e}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None
    json_data = json.loads(response.text)

    return json_data["current"]["temperature_2m"]


def convert_c2f(c_temp: float) -> float:
    """Convert Celsius to Fahrenheit
    Args:
        c_temp: A float representing the temp in Celsius

    Returns:
        float: Temperature in Fahrenheit
    """
    f_temp = (c_temp * 9/5) + 32
    return f_temp
