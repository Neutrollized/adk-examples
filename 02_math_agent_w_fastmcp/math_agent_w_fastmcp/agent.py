"""This module defines a math agent that uses FastMCP for tool execution."""
import os
import asyncio
from contextlib import AsyncExitStack

from google.adk.agents.llm_agent import LlmAgent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.tools.tool_context import ToolContext
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, SseServerParams


#-----------------
# settings
#-----------------
# Model to be used by the agent
model="gemini-2.0-flash"
# URL for the FastMCP server
fastmcp_server_url=os.environ.get("FASTMCP_SERVER_URL")

APP_NAME = "math_app"
USER_ID = "user_123"


#-----------------
# agents
#-----------------
root_agent = LlmAgent(
    name="math_agent",
    model=model,
    instruction=(
        "You are a helpful AI assistant designed to provide accurate and useful information. Do not do any math yourself, but answer the user's question correctly."
    ),
    tools=[
        MCPToolset(
            connection_params=SseServerParams(
                url=fastmcp_server_url + "/sse",
            )
        )
    ],
)


#--------------------
# session & runner
#--------------------
session_service = InMemorySessionService()
session = session_service.create_session(app_name=APP_NAME, user_id=USER_ID)    # session_id will be auto-generated of none specified

runner = Runner(agent=root_agent, app_name=APP_NAME, session_service=session_service)
