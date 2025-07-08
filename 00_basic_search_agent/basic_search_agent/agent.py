"""This module defines a basic Google Search agent."""
from google.adk.agents.llm_agent import LlmAgent
from google.adk.tools import google_search


#-------------------
# settings
#-------------------
model="gemini-2.0-flash"


#-----------------
# agents
#-----------------
search_agent = LlmAgent(
    name="search_agent",
    model=model,
    description=(
        "Agent to answer questions using Google Search"
    ),
    instruction=(
        "I can answer your questions by searching the internet. Just ask me anything!"
    ),
    tools=[
        google_search,
    ],
)

root_agent = search_agent
