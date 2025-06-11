"""This module provides tools for weather and time related information."""
import httpx, requests
import json
from timezonefinder import TimezoneFinder
import pytz
from datetime import datetime


#-------------------
# settings
#-------------------
# SSL verification for requests
verify=True

#-------------------
# function tools
#-------------------
async def get_geocoding(city: str, country: str) -> dict:
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

async def get_geocoding_v2(city: str, country: str) -> dict:
    """Find geographical location given city and country
    Args:
        city: A string representing the name of the city.
        country: A string representing the name or country code of the country.

    Returns:
        dict: Latitude and longitude of the city, country.
    """
    url = "https://geocoding-api.open-meteo.com/v1/search"
    # https://geocoding-api.open-meteo.com/v1/search?name={city}"
    query_params = {"name": city}

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=query_params, timeout=10.0) # Added a timeout for robustness
            response.raise_for_status()  # Raise an exception for HTTP errors (4xx or 5xx)
    except httpx.TimeoutException as e:
        print(f"Timeout error: {e}")
        return None
    except httpx.RequestError as e:
        print(f"Error during request: {e}")
        return None
    except httpx.HTTPStatusError as e:
        print(f"HTTP error occurred: {e.response.status_code} - {e.response.text}")
        return None

    try:
        json_data = response.json()
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON response: {e}")
        return None

    try:
        if "results" in json_data:
            for entry in json_data["results"]:
                if "country" in entry and entry["country"].lower() == country.lower():
                    return {"latitude": entry["latitude"], "longitude": entry["longitude"]}
        return None  # If "results" key is missing or no matching country is found
    except KeyError as e:
        print(f"KeyError in parsing response: {e}")
        return None
    except TypeError as e: # Handle cases where entry might not be a dictionary
        print(f"TypeError in parsing response: {e}")
        return None


async def find_current_weather(latitude: float, longitude: float) -> float:
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

async def find_current_weather_v2(latitude: float, longitude: float) -> float:
    """Find weather given geographical location
    Args:
        latitude: A float representing the latitude of a geographical location.
        longitude: A float representing the longitude of a geographical location.

    Returns:
        float: Current temperature in Celcius, or None if an error occurs.
    """
    url = "https://api.open-meteo.com/v1/forecast"

    # https://api.open-meteo.com/v1/forcast?latitude={latitude}&longitude={longitude}&current=temperature_2m"
    # Use 'params' for cleaner and safer URL query building
    query_params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": "temperature_2m"
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=query_params, timeout=10.0) # Added a timeout for robustness
            response.raise_for_status()  # Raise an exception for HTTP errors (4xx or 5xx)
    except httpx.TimeoutException as e:
        print(f"Timeout error: {e}")
        return None
    except httpx.RequestError as e:
        print(f"Error during HTTP request: {e}")
        return None
    except httpx.HTTPStatusError as e:
        print(f"HTTP error occurred: {e.response.status_code} - {e.response.text}")
        return None

    try:
        json_data = response.json() # httpx response objects have a .json() method
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON response: {e}")
        return None

    try:
        # Safely access nested dictionary keys
        return json_data["current"]["temperature_2m"]
    except KeyError as e:
        print(f"KeyError in parsing weather data: Missing key {e}")
        return None
    except TypeError as e:
        print(f"TypeError in parsing weather data: {e}")
        return None


async def get_timezone(latitude: float, longitude: float) -> str:
    """Find timezone given geographical location
    Args:
        latitude: A float representing the latitude of a geographical location.
        longitude: A float representing the longitude of a geographical location.

    Returns:
        str: Timezone name (i.e. America/Toronto)
    """
    tf = TimezoneFinder()

    timezone_name = tf.timezone_at(lat=latitude, lng=longitude)

    if timezone_name:
        return timezone_name
    else:
        print("Could not determine the timezone for the given coordinates")
        return None


async def find_current_time_in_tz(timezone_name: str) -> str:
    """Find current time in a given timezone
    Args:
        timezone_name: A string representing the timezone name.

    Returns:
        str: DateTime in ISO format (i.e. 2025-04-24T00:00:45.358804-04:00)
    """
    try:
        tz = pytz.timezone(timezone_name)
        now = datetime.now(tz)
        return now.isoformat()
    except pytz.exceptions.UnknownTimeZoneError:
        print(f"Error: Timezone '{timezone_name}' is not recognized.")
        return None


async def convert_c2f(c_temp: float) -> float:
    """Convert Celsius to Fahrenheit
    Args:
        c_temp: A float representing the temp in Celsius

    Returns:
        float: Temperature in Fahrenheit
    """
    f_temp = (c_temp * 9/5) + 32
    return f_temp
