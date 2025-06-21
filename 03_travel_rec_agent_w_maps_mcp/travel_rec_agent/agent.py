"""This module defines agents for travel recommendations."""
import os 
from google.adk.agents.llm_agent import LlmAgent
from google.adk.tools.agent_tool import AgentTool
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioServerParameters

from . import prompt


#-------------------
# settings
#-------------------
model="gemini-2.5-flash"
google_maps_api_key=os.getenv("GOOGLE_MAPS_API_KEY")


#-----------------
# agents
#-----------------
maps_agent = LlmAgent(
    name="maps_agent",
    model=model,
    instruction=prompt.MAPS_AGENT_PROMPT,
    tools=[
        MCPToolset(
            connection_params=StdioServerParameters(
                command='npx',
                args=[
                    "-y",
                    "@modelcontextprotocol/server-google-maps",
                ],
                # Pass the API key as an env var to the npx process
                # This is how the MCP server for Google Maps expects the key.
                env={
                    "GOOGLE_MAPS_API_KEY": google_maps_api_key
                },
            ),
            # You can filter for specific Map tools if needed:
            # tool_filter=['search_places', 'get_distance_matrix', 'get_directions']
        )
    ],
)

travel_rec_agent = LlmAgent(
    name="travel_rec_agent",
    model=model,
    instruction=prompt.TRAVEL_RECOMMENDER_PROMPT,
    tools=[
        AgentTool(agent=maps_agent),
    ],
)

root_agent = travel_rec_agent
