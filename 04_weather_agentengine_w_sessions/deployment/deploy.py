import os
import vertexai

from absl import app, flags
from dotenv import load_dotenv
from vertexai import agent_engines
from vertexai.preview.reasoning_engines import AdkApp

import sys
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.join(current_dir, os.pardir)
sys.path.insert(0, project_root)

from weather_agentengine.agent import root_agent


#-------------------------
# config
#-------------------------
project_id = os.getenv('AE_PROJECT_ID')
location = os.getenv('AE_LOCATION')
staging_bucket = os.getenv('AE_STAGING_BUCKET') # without gs://



FLAGS = flags.FLAGS
flags.DEFINE_string("resource_id", None, "ReasoningEngine resource ID.")

flags.DEFINE_bool("list", False, "List all agents.")
flags.DEFINE_bool("create", False, "Creates a new agent.")
flags.DEFINE_bool("delete", False, "Deletes an existing agent.")
flags.mark_bool_flags_as_mutual_exclusive(["create", "delete"])


def create() -> None:
    """Creates an agent engine for Weather."""
    adk_app = AdkApp(agent=root_agent, enable_tracing=True)

    remote_agent = agent_engines.create(
        adk_app,
        display_name=root_agent.name,
        requirements=[
            "google-adk (==1.5.0)",
            "google-cloud-aiplatform[adk,agent_engines] (>=1.100.0)",
            "google-genai (>=1.21.1)",
            "absl-py (>=2.2.1,<3.0.0)",
            "grpcio (==1.67.1)",    # suppresses some absl warnings
            "dotenv (== 0.9.9)",
            "pytz (==2025.2)",
            "timezonefinder (==6.5.9)",
        ],
        extra_packages=[
            "weather_agentengine/agent.py",
            "weather_agentengine/tools/tools.py",
        ],
    )
    print(f"Created remote agent: {remote_agent.resource_name}")


def delete(resource_id: str) -> None:
    remote_agent = agent_engines.get(resource_id)
    remote_agent.delete(force=True)
    print(f"Deleted remote agent: {resource_id}")


def list_agents() -> None:
    remote_agents = agent_engines.list()
    template = """
{agent.name} ("{agent.display_name}")
- Create time: {agent.create_time}
- Update time: {agent.update_time}
"""
    remote_agents_string = "\n".join(
        template.format(agent=agent) for agent in remote_agents
    )
    print(f"All remote agents:\n{remote_agents_string}")


def main(argv: list[str]) -> None:
    del argv  # unused
    load_dotenv()

    print(f"PROJECT: {project_id}")
    print(f"LOCATION: {location}")
    print(f"BUCKET: {staging_bucket}")

    if not project_id:
        print("Missing required environment variable: AE_PROJECT_ID")
        return
    elif not location:
        print("Missing required environment variable: AE_LOCATION")
        return
    elif not staging_bucket:
        print(
            "Missing required environment variable: AE_STAGING_BUCKET"
        )
        return

    # setup env
    # https://cloud.google.com/vertex-ai/generative-ai/docs/agent-engine/set-up#sdk-import
    vertexai.init(
        project=project_id,
        location=location,
        staging_bucket=f"gs://{staging_bucket}",
    )

    if FLAGS.list:
        list_agents()
    elif FLAGS.create:
        create()
    elif FLAGS.delete:
        if not FLAGS.resource_id:
            print("resource_id is required for delete")
            return
        delete(FLAGS.resource_id)
    else:
        print("Unknown command")


if __name__ == "__main__":
    app.run(main)
