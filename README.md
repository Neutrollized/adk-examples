# Agent Development Kit (ADK) examples

Repo with example code for building various types of agents using [ADK](https://google.github.io/adk-docs/)

- `.env` file in your agent's folder
```
GOOGLE_GENAI_USE_VERTEXAI=TRUE
GOOGLE_CLOUD_PROJECT=myproject-123
GOOGLE_CLOUD_LOCATION=us-central1
```

**NOTE:** while you can use any location you wish, not all locations supports every Gemini model


## Examples
1. Simple [Weather and Time agent](./01_weather_time_agent/) that uses [function tools](https://google.github.io/adk-docs/tools/function-tools/) to find latitude & longitude of a given city, country and its weather and time (timezone-adjusted).  Uses sub-agents to handle specific tasks, each with its own persona.  You can find a short write-up of it on my [Medium](https://medium.com/google-cloud/getting-started-with-agent-development-kit-function-tools-3f038ee646ea).

2. Model Context Protocol (MCP) example that uses FastMCP and ngrok to host the [MCP server](./02_math_agent_w_fastmcp/mcp_server/) which the [math agent](./02_math_agent_w_fastmcp/) connects to get tools to help it perform basic math (add/subtract/multiply/divide). Read about this on my [Medium](https://medium.com/google-cloud/developing-with-agent-development-kit-featuring-fastmcp-ngrok-807c552b90fd).
