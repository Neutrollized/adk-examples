import asyncio
from google.adk.evaluation.agent_evaluator import AgentEvaluator

import os
import pytest
from dotenv import find_dotenv, load_dotenv


@pytest.fixture(scope="session", autouse=True)
def load_env():
    load_dotenv(find_dotenv(".env"))

def test_evalset_weather():
    """Test the agent's basic ability via a session file."""
    AgentEvaluator.find_config_for_test_file("eval/data/test_config.json")
    AgentEvaluator.evaluate(
        agent_module="weather_time_agent",
        eval_dataset_file_path_or_dir=os.path.join(os.path.dirname(__file__), "eval/data/weather.evalset.json"),
        num_runs=1
    )
