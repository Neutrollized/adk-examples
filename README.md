# Agent Development Kit (ADK) examples

Repo with example code for building various types of agents using [ADK](https://google.github.io/adk-docs/)

## Setup
- install required Python packages/modules for the example you want to run: `pip install -r requirements.txt`

- `.env` file in your agent's folder (Google AI Studio)
```
GOOGLE_GENAI_USE_VERTEXAI=FALSE
GOOGLE_API_KEY=a1b2c3yourapikeyherex7y8z9
```

- `.env` file in your agent's folder (Vertex AI)
```
GOOGLE_GENAI_USE_VERTEXAI=TRUE
GOOGLE_CLOUD_PROJECT=myproject-123
GOOGLE_CLOUD_LOCATION=us-central1
```
**NOTE:** while you can use any location you wish, not all locations supports every Gemini model


## Examples
0. A very basic agent that leverages Google Search as the tool to help the user find answers.  If you're new to programming and/or ADK, I suggest you start here :)

1. Simple [Weather and Time agent](./01_weather_time_agent/) that uses [function tools](https://google.github.io/adk-docs/tools/function-tools/) to find latitude & longitude of a given city, country and its weather and time (timezone-adjusted).  Uses sub-agents to handle specific tasks, each with its own persona.  You can find a short write-up of it on my [Medium](https://medium.com/google-cloud/getting-started-with-agent-development-kit-function-tools-3f038ee646ea).  I wrote a follow-up article about [Agent Evaluation](https://medium.com/google-cloud/testing-with-agent-development-kit-agent-evaluations-76a9eec27965) and added the evalset and instructions to for this particular agent example. I then added a [callback function](https://medium.com/google-cloud/developing-with-agent-development-kit-using-callbacks-7a6285139432) to make the agent a little more robust.

2. Model Context Protocol (MCP) example that uses FastMCP and ngrok to host the [MCP server](./02_math_agent_w_fastmcp/mcp_server/) which the [math agent](./02_math_agent_w_fastmcp/) connects to get tools to help it perform basic math (add/subtract/multiply/divide). Read about this on my [Medium](https://medium.com/google-cloud/developing-with-agent-development-kit-featuring-fastmcp-ngrok-807c552b90fd).

3. Another MCP example.  This time it is a [travel recommendation agent](./03_travel_rec_agent_w_maps_mcp/) that uses a local Google Maps Platform MCP server (via Stdio) to find attractions and restaurants near a give origin location.  In its current form, the directions and travel distance returned can be quite wrong and hence I wouldn't really rely on it for directions. I built my own [Google Maps MCP server (in Python)](https://github.com/Neutrollized/google-maps-mcp-server) that I'll be using going forward in future examples.
