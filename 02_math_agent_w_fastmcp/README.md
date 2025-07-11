# Math Agent with FastMCP Server
This agent performs basic arithmetic operations. It builds on the [MCP tools example](https://google.github.io/adk-docs/tools/mcp-tools/#example-3-fastmcp-server) from the ADK documentation.
The agent uses a [FastMCP server](./math_agent_w_fastmcp/mcp_server/server.py) that provides tools for:
- Addition
- Subtraction
- Multiplication
- Division (float result)
- Quotient (integer result)

Instead of deploying to [Cloud Run](https://cloud.google.com/run), this example uses [ngrok](https://ngrok.com/) to facilitate faster development and local testing.


## Running Agent
- [start the FastMCP server](./math_agent_w_fastmcp/mcp_server/README.md)
- export the `FASTMCP_SERVER_URL` environment variable (whether that's a Cloud Run URL or ngrok generated URL)

- ADK dev UI (http://localhost:8000):
```
adk web
```

- ADK cli/terminal:
```
adk run math_agent
```

- sample terminal output from `adk run math_agent_w_fastmcp`:
```console
Running agent math_agent, type exit to exit.
[user]: what's 6/2+9*9
[math_agent]: 6 / 2 is 3 and 9 * 9 is 81. So the answer is 3 + 81 = 84.

[user]: Alice brought 12 pizzas. Bob brought 8 pizzas. Charlie brought 5 pizzas. There are 8 slices per pizza. If there are 50 people sharing the pizzas, how many slices do each person get?
[math_agent]: Alice brought 12 pizzas, Bob brought 8 pizzas, and Charlie brought 5 pizzas. So there are 12 + 8 + 5 = 25 pizzas in total.
There are 8 slices per pizza, so there are 25 * 8 = 200 slices in total.
If there are 50 people sharing the pizzas, each person gets 200 / 50 = 4 slices.
So each person gets 4 slices.

[user]: Each car has 5 tires (4 on the car + 1 spare in the trunk), so how many tires would there be if there are 20 cars?
[math_agent]: If each car has 5 tires, and there are 20 cars, then there would be a total of 5 * 20 = 100 tires.
So the answer is 100.

[user]: Frank has 5 cats and each cat has 2 ears, how many ears are there in total (including Frank)?
[math_agent]: Frank has 2 ears and each of his 5 cats has 2 ears, so there are 5 * 2 = 10 cat ears. In total, there are 2 + 10 = 12 ears.
So the answer is 12.

[user]: exit
```

(I tried to trick it with the last question)


## Agent Evaluation
The following testing commands are executed from the `02_math_agent_w_fastmcp` directory.

### adk eval
- [documentation](https://google.github.io/adk-docs/evaluate/#3-adk-eval-run-evaluations-via-the-cli)
```sh
adk eval \
    --config_file_path eval/data/test_config.json \
    --print_detailed_results \
    math_agent \
    eval/data/math.evalset.json
```

- sample output (**NOTE**: you may see some SSE client async errors, but just let it run its course):
```console
Using evaluation creiteria: {'tool_trajectory_avg_score': 0.8, 'response_match_score': 0.65}
Running Eval: eval/data/math.evalset.json:case0e02e6
...
...
Computing metrics with a total of 1 Vertex Gen AI Evaluation Service API requests.
100%|█████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00,  2.80it/s]
All 1 metric requests are successfully computed.
Evaluation Took:0.36107562499819323 seconds
Result: ✅ Passed

*********************************************************************
Eval Run Summary
eval/data/math.evalset.json:
  Tests passed: 1
  Tests failed: 0
*********************************************************************
{
  "eval_set_file": "eval/data/math.evalset.json",
  "eval_set_id": "eval/data/math.evalset.json",
  "eval_id": "case0e02e6",
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
      "score": 0.8430088116666666,
      "eval_status": 1
    }
  ],
  "eval_metric_result_per_invocation": [
...
...
    {
      "actual_invocation": {
        "invocation_id": "e-4ac96e30-97b0-4f5a-9e08-eceba145de18",
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
              "text": "what can you do?"
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
              "text": "I can perform basic arithmetic operations, including addition, subtraction, multiplication, division, and quotient (division ignoring remainder). Just let me know what you'd like me to calculate!\n"
            }
          ],
          "role": "model"
        },
        "intermediate_data": {
          "tool_uses": [],
          "intermediate_responses": []
        },
        "creation_timestamp": 0.0
      },
      "expected_invocation": {
        "invocation_id": "e-f1ce6d50-8fef-4876-84fc-9de16f6c4e60",
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
              "text": "what can you do?"
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
              "text": "I can perform basic arithmetic operations, including addition, subtraction, multiplication, division, and quotient (division ignoring remainder). Just let me know what you'd like me to calculate!\n"
            }
          ],
          "role": null
        },
        "intermediate_data": {
          "tool_uses": [],
          "intermediate_responses": []
        },
        "creation_timestamp": 1748270933.667832
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
          "score": 1.0,
          "eval_status": 1
        }
      ]
    },
...
...
    {
      "actual_invocation": {
        "invocation_id": "e-49b22949-1790-4fc2-976a-0cedc000a642",
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
              "text": "what about 6/3+8*5?"
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
              "text": "Okay, 6 / 3 = 2.0 and 8 * 5 = 40. So, 2.0 + 40 = 42.0\n"
            }
          ],
          "role": "model"
        },
        "intermediate_data": {
          "tool_uses": [
            {
              "id": "adk-016d0365-3ae2-451d-98d3-0409c15ab9c8",
              "args": {
                "a": 6,
                "b": 3
              },
              "name": "divide"
            },
            {
              "id": "adk-88f3df8e-1114-4d20-81ae-1b2b0045b73a",
              "args": {
                "a": 8,
                "b": 5
              },
              "name": "multiply"
            }
          ],
          "intermediate_responses": []
        },
        "creation_timestamp": 0.0
      },
      "expected_invocation": {
        "invocation_id": "e-67b44d44-3fe4-4942-81c4-d999c4c17f36",
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
              "text": "what about 6/3+8*5?"
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
              "text": "6 / 3 = 2.0 and 8 * 5 = 40. So, 2.0 + 40 = 42.0\n"
            }
          ],
          "role": null
        },
        "intermediate_data": {
          "tool_uses": [
            {
              "id": "adk-cf96b4cd-ac76-430c-96fe-e33f5d7a2ffd",
              "args": {
                "a": 6,
                "b": 3
              },
              "name": "divide"
            },
            {
              "id": "adk-9bdeaf03-5332-4807-bbdf-dfe60ffbc291",
              "args": {
                "a": 8,
                "b": 5
              },
              "name": "multiply"
            }
          ],
          "intermediate_responses": []
        },
        "creation_timestamp": 1748270964.123317
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
          "score": 0.9655172,
          "eval_status": 1
        }
      ]
    },
...
...
  ],
  "session_id": "___eval___session___a5b9345c-aba5-4bd1-933b-05be4e050d68",
  "session_details": null,
  "user_id": "user"
}
```
