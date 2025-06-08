"""This module defines agents for weather and time inquiries."""
import logging
import sys
from google.adk.agents.llm_agent import LlmAgent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.tools import FunctionTool
from google.adk.tools.tool_context import ToolContext
from google.adk.tools.base_tool import BaseTool
from typing import Optional, Dict, Any
from google.genai import types  # this is needed for GenerateContentConfig

from .tools.tools import (
    get_geocoding,
    get_timezone,
    find_current_weather,
    find_current_time_in_tz,
    convert_c2f,
)

# https://google.github.io/adk-docs/tools/#tool-types-in-adk
geocoding_tool = FunctionTool(func=get_geocoding)
timezone_tool = FunctionTool(func=get_timezone)
current_weather_tool = FunctionTool(func=find_current_weather)
current_time_tool = FunctionTool(func=find_current_time_in_tz)
celsius2fahrenheit_tool = FunctionTool(func=convert_c2f)


#-------------------
# settings
#-------------------
country_abbrev_dict = {
    # keys should be all uppercase here
    "USA": "United States",
    "UK": "United Kingdom",
    "GB": "United Kingdom",
    "UAE": "United Arab Emirates",
    "DRC": "DR Congo",
    "CAR": "Central African Republic"
}

logger=logging.getLogger(__name__)
model="gemini-2.0-flash"

APP_NAME = "weather_time_app"
USER_ID = "user_1234"


#-------------------
# callbacks
#-------------------
def country_name_before_tool_modifier(tool: BaseTool, args: Dict[str, Any], tool_context: ToolContext) -> Optional[Dict]:
    """Inspects/modifies tool args or skips the tool call."""
    agent_name = tool_context.agent_name
    tool_name = tool.name
    print(f"[Callback] Before tool call for tool '{tool_name}' in agent '{agent_name}'")
    print(f"[Callback] Original args: {args}")

    # need to provide the Python function name here not the wrapped FunctionTool name...
    if tool_name == 'get_geocoding' and args.get('country', '').upper() in country_abbrev_dict:
        print(f"[Callback] Detected {args.get('country', '').upper()}. Modifying arg to {country_abbrev_dict[args.get('country', '').upper()]}.")
        args['country'] = country_abbrev_dict[args.get('country', '').upper()]
        print(f"[Callback] Modified args: {args}")
        return None

    return None


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
        geocoding_tool,
        current_weather_tool,
        convert_c2f
    ],
    before_tool_callback=country_name_before_tool_modifier
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
        geocoding_tool,
        timezone_tool,
        current_time_tool
    ],
    before_tool_callback=country_name_before_tool_modifier
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
