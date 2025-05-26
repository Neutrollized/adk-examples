# Weather & Time agent

This agent can tell you the date/time and weather of a given city and country. It utilizes two sub-agents:
- `time_agent`: Handles queries related to the current date and time.
- `weather_agent`: Handles queries related to the current weather.

## Running Agent
- ADK dev UI (http://localhost:8000):
```
adk web
```

- ADK cli/terminal:
```
adk run weather_time_agent
```

- sample terminal output from `adk run weather_time_agent`:
```console
Running agent root_agent, type exit to exit.
user: what's the time in pune, india?
[time_agent]: The date be April 24, 2025 and the time be 7:17 PM.

user: what about london, uk?
[time_agent]: I be havin' trouble findin' that location, matey. Can you be more specific? Perhaps tryin' "United Kingdom" instead of "UK"?

user: united kingdom
[time_agent]: The date be April 24, 2025 and the time be 2:48 PM.

user: what's the weather there?
[weather_agent]: The current temperature in London is 14.9 degrees Celsius.

user: what about cypress?
[weather_agent]: Do you mean the country Cyprus, or a city named Cypress in another country? If it is a city, please also specify the country.

user: nicosia in cyprus
[weather_agent]: The current temperature in Nicosia, Cyprus is 20.3 degrees Celsius.

user: exit
```

Notice how it was about to correct me on the misspelling of "Cyprus" and ask for validation.


## Agent Evaluation
The following testing commands are executed from the `01_weather_time_agent` directory.

### pytest (unit tests)
```sh
pytest -v tests
```

### adk eval
- [documentation](https://google.github.io/adk-docs/evaluate/#3-adk-eval-run-evaluations-via-the-cli)
```sh
adk eval \
    --config_file_path eval/data/test_config.json \
    --print_detailed_results \
    weather_time_agent \
    eval/data/weather.evalset.json
```

- sample (partial) output:
```console
Using evaluation creiteria: {'tool_trajectory_avg_score': 0.8, 'response_match_score': 0.65}
Running Eval: eval/data/weather.evalset.json:case7cfcd8
Warning: there are non-text parts in the response: ['function_call'], returning concatenated text result from text parts. Check the full candidates.content.parts accessor to get the full model response.
...
...
Computing metrics with a total of 1 Vertex Gen AI Evaluation Service API requests.
100%|███████████████████████████████████████████████████████████████| 1/1 [00:00<00:00,  2.87it/s]
All 1 metric requests are successfully computed.
Evaluation Took:0.3526891670007899 seconds
Result: ✅ Passed

*********************************************************************
Eval Run Summary
eval/data/weather.evalset.json:
  Tests passed: 1
  Tests failed: 0
*********************************************************************
{
  "eval_set_file": "eval/data/weather.evalset.json",
  "eval_set_id": "eval/data/weather.evalset.json",
  "eval_id": "case7cfcd8",
  "final_eval_status": 1,
  "eval_metric_results": [],
  "overall_eval_metric_results": [
    {
      "metric_name": "tool_trajectory_avg_score",
      "threshold": 0.8,
      "score": 1.0,
      "eval_status": 1
    },
    {
      "metric_name": "response_match_score",
      "threshold": 0.65,
      "score": 0.810145042,
      "eval_status": 1
    }
  ],
  "eval_metric_result_per_invocation": [
...
...
    {
      "actual_invocation": {
        "invocation_id": "e-3e8f40aa-8b17-4de1-be35-b3e40e23338b",
        "user_content": {
          "parts": [
            {
              "video_metadata": null,
              "thought": null,
              "inline_data": null,
              "code_execution_result": null,
              "executable_code": null,
              "file_data": null,
              "function_call": null,
              "function_response": null,
              "text": "what about in sydney, australia?"
            }
          ],
          "role": "user"
        },
        "final_response": {
          "parts": [
            {
              "video_metadata": null,
              "thought": null,
              "inline_data": null,
              "code_execution_result": null,
              "executable_code": null,
              "file_data": null,
              "function_call": null,
              "function_response": null,
              "text": "The weather in Sydney, Australia is 16.3 degrees Celsius.\n"
            }
          ],
          "role": "model"
        },
        "intermediate_data": {
          "tool_uses": [
            {
              "id": "adk-2a63ce76-5b1f-4c71-9540-ac3fc528f3d5",
              "args": {
                "country": "australia",
                "city": "sydney"
              },
              "name": "get_geocoding"
            },
            {
              "id": "adk-52a8d7c9-1a8b-438a-be6a-4783c5a977e4",
              "args": {
                "latitude": -33.86785,
                "longitude": 151.20732
              },
              "name": "find_current_weather"
            }
          ],
          "intermediate_responses": []
        },
        "creation_timestamp": 0.0
      },
      "expected_invocation": {
        "invocation_id": "e-51b3a137-9239-4503-857a-2ed88d811ec8",
        "user_content": {
          "parts": [
            {
              "video_metadata": null,
              "thought": null,
              "inline_data": null,
              "code_execution_result": null,
              "executable_code": null,
              "file_data": null,
              "function_call": null,
              "function_response": null,
              "text": "what about in sydney, australia?"
            }
          ],
          "role": "user"
        },
        "final_response": {
          "parts": [
            {
              "video_metadata": null,
              "thought": null,
              "inline_data": null,
              "code_execution_result": null,
              "executable_code": null,
              "file_data": null,
              "function_call": null,
              "function_response": null,
              "text": "The weather in Sydney, Australia is 15.1 degrees Celsius.\n"
            }
          ],
          "role": null
        },
        "intermediate_data": {
          "tool_uses": [
            {
              "id": "adk-be48bf86-3fac-4f16-a6b0-81428ac5f7c8",
              "args": {
                "country": "australia",
                "city": "sydney"
              },
              "name": "get_geocoding"
            },
            {
              "id": "adk-6905da5e-9474-4346-b5ef-58bbefd00871",
              "args": {
                "longitude": 151.20732,
                "latitude": -33.86785
              },
              "name": "find_current_weather"
            }
          ],
          "intermediate_responses": []
        },
        "creation_timestamp": 1748129942.627008
      },
      "eval_metric_results": [
        {
          "metric_name": "tool_trajectory_avg_score",
          "threshold": 0.8,
          "score": 1.0,
          "eval_status": 1
        },
        {
          "metric_name": "response_match_score",
          "threshold": 0.65,
          "score": 0.8,
          "eval_status": 1
        }
      ]
    },
...
...
  ],
  "session_id": "___eval___session___66621041-62b4-4d1c-ac68-f5716c702546",
  "session_details": null,
  "user_id": "user"
}
```
