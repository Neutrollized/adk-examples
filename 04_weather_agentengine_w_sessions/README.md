# Weather Agent using AgentEngine

This agent can tell you the weather of a given city and country (it's a slimmed down version of the [01_weather_time_agent](../01_weather_time_agent/)).  I've added a model callback function that looks at the initial state for a user and if `{"units": "imperial"}` is set, then the response will return the temperature in Fahrenheit (default: Celsius). 


## Local testing
This is the cost-effective way of testing sessions and state, but the conversation is not interactive.

```sh
python weather_agentengine/test_agent_local.py
```

- sample output:
```console
---------- USER 1 ---------------

[Model Callback] Before model call for user unit preference: imperial
[Model Callback] Modified system instruction to: 'You are a helpful agent who can answer user questions about the weather in a city and country.

You are an agent. Your internal name is "weather_agent".

 The description about you is "Agent to answer questions about the weather in a city." Return units in imperial.'
Warning: there are non-text parts in the response: ['function_call'], returning concatenated text result from text parts. Check the full candidates.content.parts accessor to get the full model response.
[Tool Callback] Detected USA. Modifying arg to United States.
[Tool Callback] Modified args: {'city': 'Chicago', 'country': 'United States'}
[Model Callback] Before model call for user unit preference: imperial
[Model Callback] Modified system instruction to: 'You are a helpful agent who can answer user questions about the weather in a city and country.

You are an agent. Your internal name is "weather_agent".

 The description about you is "Agent to answer questions about the weather in a city." Return units in imperial.'
Warning: there are non-text parts in the response: ['function_call'], returning concatenated text result from text parts. Check the full candidates.content.parts accessor to get the full model response.
[Model Callback] Before model call for user unit preference: imperial
[Model Callback] Modified system instruction to: 'You are a helpful agent who can answer user questions about the weather in a city and country.

You are an agent. Your internal name is "weather_agent".

 The description about you is "Agent to answer questions about the weather in a city." Return units in imperial.'

FINAL RESPONSE: The current temperature in Chicago is 85.46°F.

---------- USER 2 ---------------

[Model Callback] Before model call for user unit preference (default): metric
[Model Callback] Modified system instruction to: 'You are a helpful agent who can answer user questions about the weather in a city and country.

You are an agent. Your internal name is "weather_agent".

 The description about you is "Agent to answer questions about the weather in a city." Return units in metric.'
Warning: there are non-text parts in the response: ['function_call'], returning concatenated text result from text parts. Check the full candidates.content.parts accessor to get the full model response.
[Model Callback] Before model call for user unit preference (default): metric
[Model Callback] Modified system instruction to: 'You are a helpful agent who can answer user questions about the weather in a city and country.

You are an agent. Your internal name is "weather_agent".

 The description about you is "Agent to answer questions about the weather in a city." Return units in metric.'
Warning: there are non-text parts in the response: ['function_call'], returning concatenated text result from text parts. Check the full candidates.content.parts accessor to get the full model response.
[Model Callback] Before model call for user unit preference (default): metric
[Model Callback] Modified system instruction to: 'You are a helpful agent who can answer user questions about the weather in a city and country.

You are an agent. Your internal name is "weather_agent".

 The description about you is "Agent to answer questions about the weather in a city." Return units in metric.'

FINAL RESPONSE: The weather in Tokyo, Japan is 23.2 degrees Celsius.
```


## Deploying to Agent Engine
This method deploys to Vertex AI's [Agent Engine](https://cloud.google.com/vertex-ai/generative-ai/docs/agent-engine/overview) and you get to have.  Agent Engine is a fully managed platform for building, deploying, managing, and scaling AI agents in production.  It will cost you to run this, so don't forget to cleanup after you're done!

### Setup
You will need to first create a GCS bucket for GCP to use as a staging area/bucket.  In addition to that you will need to set 3 environment variables:
- `AE_PROJECT_ID`       (your GCP project ID)
- `AE_LOCATION`         (deployment location for your Agent Engine)
- `AE_STAGING_BUCKET`   (GCS bucket name, without the gs://)

Create your Agent Engine with:
```sh
python ./deployment/deploy.py --create
```

- sample output:
```console
PROJECT: my-project
LOCATION: us-central1
BUCKET: my-bucket
Identified the following requirements: {'google-cloud-aiplatform': '1.103.0', 'pydantic': '2.11.7', 'cloudpickle': '3.1.1'}
I0712 17:52:07.788920 8466767616 _utils.py:379] Identified the following requirements: {'google-cloud-aiplatform': '1.103.0', 'pydantic': '2.11.7', 'cloudpickle': '3.1.1'}
The following requirements are missing: {'pydantic', 'cloudpickle'}
W0712 17:52:07.796045 8466767616 _utils.py:386] The following requirements are missing: {'pydantic', 'cloudpickle'}
The following requirements are appended: {'pydantic==2.11.7', 'cloudpickle==3.1.1'}
I0712 17:52:07.796091 8466767616 _utils.py:393] The following requirements are appended: {'pydantic==2.11.7', 'cloudpickle==3.1.1'}
The final list of requirements: ['google-adk (==1.5.0)', 'google-cloud-aiplatform[adk,agent_engines] (>=1.100.0)', 'google-genai (>=1.21.1)', 'absl-py (>=2.2.1,<3.0.0)', 'grpcio (==1.67.1)', 'dotenv (== 0.9.9)', 'pytz (==2025.2)', 'timezonefinder (==6.5.9)', 'pydantic==2.11.7', 'cloudpickle==3.1.1']
...
...
Writing to gs://my-bucket/agent_engine/requirements.txt
I0712 17:52:09.395336 8466767616 _agent_engines.py:1007] Writing to gs://my-bucket/agent_engine/requirements.txt
Creating in-memory tarfile of extra_packages
I0712 17:52:09.395675 8466767616 _agent_engines.py:1018] Creating in-memory tarfile of extra_packages
Writing to gs://my-bucket/agent_engine/dependencies.tar.gz
I0712 17:52:09.560689 8466767616 _agent_engines.py:1027] Writing to gs://my-bucket/agent_engine/dependencies.tar.gz
Creating AgentEngine
I0712 17:52:10.176353 8466767616 base.py:85] Creating AgentEngine
Create AgentEngine backing LRO: projects/1234567890/locations/us-central1/reasoningEngines/8769942237652975616/operations/8230694696909799424
...
...
I0712 17:55:12.705086 8466767616 _agent_engines.py:526] agent_engine = vertexai.agent_engines.get('projects/1234567890/locations/us-central1/reasoningEngines/8769942237652975616')
Created remote agent: projects/1234567890/locations/us-central1/reasoningEngines/8769942237652975616
```

```sh
python ./deployment/deploy.py --list
```

- sample output:
```
PROJECT: my-project
LOCATION: us-central1
BUCKET: my-bucket
All remote agents:

8769942237652975616 ("weather_agent")
- Create time: 2025-07-12 22:23:29.346034+00:00
- Update time: 2025-07-12 22:26:29.204612+00:00
```


### Creating a User & Session
I've included some Python and shell scripts for you to run.  It has predefined settings for 2 different users, **user123** and **user456**, each with its own initial state. View/edit the script to create a session for the desired user and run:
```sh
python ./adk_client.py
```

- sample output:
```console
> No saved sessions found. Creating a new session for user456...
> New session created with ID: 3724655562474913792
USER: user456
STATE: {'units': 'imperial'}
```

Edit the [`client_requests.py`](./client_requests.py) script to update agent ID and session ID, then run:
```sh
python ./client_requests.py
```

- sample output:
```console
...
...
{"content": {"parts": [{"text": "The weather in San Jose, USA is 83.48\u00b0F."}], "role": "model"}, "usage_metadata": {"candidates_token_count": 17, "candidates_tokens_details": [{"modality": "TEXT", "token_count": 17}], "prompt_token_count": 557, "prompt_tokens_details": [{"modality": "TEXT", "token_count": 557}], "thoughts_token_count": 122, "total_token_count": 696, "traffic_type": "ON_DEMAND"}, "invocation_id": "e-7ed6087c-d8dc-402e-bbfe-9f7879c57b21", "author": "weather_agent", "actions": {"state_delta": {"weather_response": "The weather in San Jose, USA is 83.48\u00b0F."}, "artifact_delta": {}, "requested_auth_configs": {}}, "id": "dLuAQNRf", "timestamp": 1752359836.044323}
```

As you can see, the response is in Fahrenheit, as expected.


#### Show Agent Engine state
Because sessions are saved and managed through Vertex AI, you can query your agent's stored sessions for a given user by running the script again (which has some predefined logic in my case):
```sh
python ./adk_client.py
```

- sample output
```console
> Existing session(s) found for user456:
  - Session ID: 3724655562474913792
> Loading session 3724655562474913792
USER: user456
STATE: {'units': 'imperial', 'weather_response': 'The weather in San Jose, USA is 83.48°F.'}
```

## NOTE
You can try creating another saved session for **user123** and use send your queries to the agent via `curl` instead.  See [`rest_request.sh`](./rest_request.sh) for details.


## Cleanup
```sh
python ./deployment/deploy.py --delete --resource_id=8769942237652975616
```
