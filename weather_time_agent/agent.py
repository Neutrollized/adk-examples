import requests
import json
import sys
from timezonefinder import TimezoneFinder
import pytz
from datetime import datetime
from google.adk.agents import Agent


model="gemini-2.0-flash"


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
        response = requests.get(query)
    except requests.exceptions.Timeout as e:
        print(f"Timeout error: {e}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None
    json_data = json.loads(response.text)

    for entry in json_data["results"]:
        try:
            #if entry["country"].lower() == country.lower() or entry["country_code"].lower() == country.lower():
            if entry["country"].lower() == country.lower():
                return {"latitude": entry["latitude"], "longitude": entry["longitude"]}
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
        response = requests.get(query)
    except requests.exceptions.Timeout as e:
        print(f"Timeout error: {e}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None
    json_data = json.loads(response.text)

    return json_data["current"]["temperature_2m"]


def get_timezone(latitude: float, longitude: float) -> str:
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


def find_current_time_in_tz(timezone_name: str) -> str:
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


#-----------------
# agents
#-----------------
weather_agent = Agent(
    name="weather_agent",
    model=model,
    description=(
        "Agent to answer questions about the weather in a city."
    ),
    instruction=(
        "You are a helpful agent who can answer user questions about the weather in a city and country."
    ),
    tools=[
        get_geocoding,
        find_current_weather
    ],
)

time_agent = Agent(
    name="time_agent",
    model=model,
    description=(
        "Agent to answer questions about the date and time of a city."
    ),
    instruction=(
        "You are a helpful pirate who can answer user questions about the date and time of a city. Don't give the response in ISO format.  Give the date and time."
    ),
    tools=[
        get_geocoding,
        get_timezone,
        find_current_time_in_tz
    ],
)

root_agent = Agent(
    name="root_agent",
    model=model,
    description=(
        "Root agent that delegates to sub-agents. I can help you answer questions about the current date/time and weather in any city."
    ),
    sub_agents=[
        weather_agent,
        time_agent
    ],
)
