import asyncio
import json
import requests
import sys
from google.adk.agents.llm_agent import LlmAgent
from google.genai import types  # this is needed for GenerateContentConfig
from google.genai.types import Content, Part

# used by callbacks
from google.adk.agents.callback_context import CallbackContext
from google.adk.models import LlmResponse, LlmRequest
from google.adk.tools.tool_context import ToolContext
from google.adk.tools.base_tool import BaseTool
from typing import Optional, Dict, Any

# import tools
from tools.tools import (
    get_geocoding,
    find_current_weather,
    convert_c2f,
)

#-------------------
# settings
#-------------------
model="gemini-2.5-flash"

verify=True

COUNTRY_ABBREV_DICT = {
    # keys should be all uppercase here
    "USA": "United States",
    "UK": "United Kingdom",
    "GB": "United Kingdom",
    "UAE": "United Arab Emirates",
    "DRC": "DR Congo",
    "CAR": "Central African Republic"
}


#-------------------
# callbacks
#-------------------
def query_before_model_units_modifier(callback_context: CallbackContext, llm_request: LlmRequest) -> Optional[LlmResponse]:
    """Inspects/modifies the LLM request or skips the call."""
    agent_name = callback_context.agent_name
    #print(f"[Model Callback] Before model call for agent: {agent_name}")

    agent_state = callback_context.state.to_dict()
    try:
        print(f"[Model Callback] Before model call for user unit preference: {agent_state["units"]}")

        # ensure system_instruction is Content and parts list exists
        original_instruction = llm_request.config.system_instruction or types.Content(role="system", parts=[])
        if not isinstance(original_instruction, types.Content):
            # handle case where it might be a string (though config expects Content)
            original_instruction = types.Content(role="system", parts=[types.Part(text=str(original_instruction))])

        units_return_type = f" Return units in {agent_state["units"]}."
        modified_text = original_instruction.parts[0].text + units_return_type
        original_instruction.parts[0].text = modified_text
        llm_request.config.system_instruction = original_instruction
        print(f"[Model Callback] Modified system instruction to: '{modified_text}'")

    except KeyError:
        print(f"[Model Callback] Before model call for user unit preference (default): metric")

        # ensure system_instruction is Content and parts list exists
        original_instruction = llm_request.config.system_instruction or types.Content(role="system", parts=[])
        if not isinstance(original_instruction, types.Content):
            # handle case where it might be a string (though config expects Content)
            original_instruction = types.Content(role="system", parts=[types.Part(text=str(original_instruction))])

        units_return_type = " Return units in metric." 
        modified_text = original_instruction.parts[0].text + units_return_type
        original_instruction.parts[0].text = modified_text
        llm_request.config.system_instruction = original_instruction
        print(f"[Model Callback] Modified system instruction to: '{modified_text}'")

    return None


def country_name_before_tool_modifier(tool: BaseTool, args: Dict[str, Any], tool_context: ToolContext) -> Optional[Dict]:
    """Inspects/modifies tool args or skips the tool call."""
    agent_name = tool_context.agent_name
    agent_state = tool_context.state.to_dict()
    tool_name = tool.name
    #print(f"[Tool Callback] Before tool call for tool '{tool_name}' in agent '{agent_name}'")
    #print(f"[Tool Callback] Original args: {args}")

    # need to provide the Python function name here not the wrapped FunctionTool name...
    if tool_name == 'get_geocoding' and args.get('country', '').upper() in COUNTRY_ABBREV_DICT:
        print(f"[Tool Callback] Detected {args.get('country', '').upper()}. Modifying arg to {COUNTRY_ABBREV_DICT[args.get('country', '').upper()]}.")
        args['country'] = COUNTRY_ABBREV_DICT[args.get('country', '').upper()]
        print(f"[Tool Callback] Modified args: {args}")
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
        get_geocoding,
        find_current_weather,
        convert_c2f,
    ],
    output_key="weather_response",
    before_model_callback=query_before_model_units_modifier,
    before_tool_callback=country_name_before_tool_modifier,
)

root_agent = weather_agent


#-----------------------
# local execution
#-----------------------
from vertexai.preview import reasoning_engines

app = reasoning_engines.AdkApp(
    agent=root_agent,
    enable_tracing=True,
)


print("\n---------- USER 1 ---------------\n")
session_user1 = app.create_session(
    user_id="user1",
    session_id="session_user1",
    state={"units": "imperial"},
)
#print(session_user1)
for event in app.stream_query(
    user_id="user1",
    session_id="session_user1",
    message="What's the weather in Chicago, USA?"
):
    #print(event)
    if "actions" in event and "weather_response" in event["actions"]["state_delta"]:
        final_response = event["actions"]["state_delta"]["weather_response"]
        print(f"\nFINAL RESPONSE: {final_response}")



print("\n---------- USER 2 ---------------\n")
session_user2 = app.create_session(
    user_id="user2",
    session_id="session_user2",
)
#print(session_user2)
for event in app.stream_query(
    user_id="user2",
    session_id="session_user2",
    message="What's the weather in Tokyo, Japan?"
):
    #print(event)
    if "actions" in event and "weather_response" in event["actions"]["state_delta"]:
        final_response = event["actions"]["state_delta"]["weather_response"]
        print(f"\nFINAL RESPONSE: {final_response}")

