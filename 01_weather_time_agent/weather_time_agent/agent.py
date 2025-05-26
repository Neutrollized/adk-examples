"""This module defines agents for weather and time inquiries."""
import logging
import sys
from google.adk.agents.llm_agent import LlmAgent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
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

APP_NAME = "weather_time_app"
USER_ID = "user_1234"


#-----------------
# agents
#-----------------
# Agent specifically for handling weather-related queries.
weather_agent = LlmAgent(
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
time_agent = LlmAgent(
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
root_agent = LlmAgent(
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


#--------------------
# session & runner
#--------------------
session_service = InMemorySessionService()
session = session_service.create_session(app_name=APP_NAME, user_id=USER_ID)    # session_id will be auto-generated of none specified

runner = Runner(agent=root_agent, app_name=APP_NAME, session_service=session_service)
