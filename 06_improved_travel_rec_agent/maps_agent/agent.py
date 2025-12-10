import os
import asyncio
from contextlib import AsyncExitStack

from google.adk.agents.llm_agent import LlmAgent
from google.adk.tools.google_search_tool import GoogleSearchTool
from google.adk.tools.agent_tool import AgentTool
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioServerParameters

from google.genai import types
from . import prompt


#-----------------
# settings
#-----------------
# Model to be used by the agent
model="gemini-2.5-flash"
google_maps_api_key=os.getenv("GOOGLE_MAPS_API_KEY")


#-----------------
# agents
#-----------------
gmaps_agent = LlmAgent(
    name="gmaps_agent",
    model=model,
    generate_content_config=types.GenerateContentConfig(
        temperature=0.9,
        top_p=0.9,
        top_k=40,
    ),
    instruction=prompt.MAPS_AGENT_PROMPT,
    tools=[
        MCPToolset(
            connection_params=StdioServerParameters(
                command='fastmcp',
                args=[
                    "run",
                    "maps_agent/server.py"
                ],
                env={
                    "GOOGLE_MAPS_API_KEY": google_maps_api_key
                },
            ),
        ),
    ],
)

travel_rec_agent = LlmAgent(
    name="travel_rec_agent",
    model=model,
    instruction=prompt.TRAVEL_RECOMMENDER_PROMPT,
    tools=[
        AgentTool(agent=gmaps_agent),
        GoogleSearchTool(bypass_multi_tools_limit=True),
    ],
)

root_agent = travel_rec_agent
