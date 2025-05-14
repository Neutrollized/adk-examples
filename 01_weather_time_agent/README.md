# Weather & Time agent

Agent that can tell you the date/time and weather of a given city, country. Uses sub-agents to handle weather and date/time separately. 

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


## Testing
The following testing commands are executed from the `01_weather_time_agent` directory.

**NOTE**: currently there are some bugs with pytest test and ADK evaluations

### pytest
- [documentation](https://google.github.io/adk-docs/evaluate/#2-pytest-run-tests-programmatically)
```sh
PYTHONTRACEMALLOC=1 pytest -v eval
```

### adk eval
- [documentation](https://google.github.io/adk-docs/evaluate/#3-adk-eval-run-evaluations-via-the-cli)
```sh
adk eval \
    weather_time_agent \
    eval/data/weather.test.json:eval/data/weather_fail.test.json \
    --config_file_path eval/data/test_config.json
```
