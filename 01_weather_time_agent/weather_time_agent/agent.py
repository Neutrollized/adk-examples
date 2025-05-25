"""This module defines agents for weather and time inquiries."""
import logging
import sys
from google.adk.agents import Agent
from google.genai import types  # this is needed for GenerateContentConfig

from .tools.tools import (
    get_geocoding,
    get_timezone,
    find_current_weather,
    find_current_time_in_tz,
)


#-------------------
# settings
#-------------------
logger=logging.getLogger(__name__)
model="gemini-2.0-flash"


#-----------------
# agents
#-----------------
# Agent specifically for handling weather-related queries.
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

# Agent specifically for handling time-related queries.
time_agent = Agent(
    name="time_agent",
    model=model,
    generate_content_config=types.GenerateContentConfig(
        temperature=0.9,
        top_p=0.9,
        top_k=40,
        max_output_tokens=250
    ),
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

# Root agent that directs queries to the appropriate sub-agent (weather or time).
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
