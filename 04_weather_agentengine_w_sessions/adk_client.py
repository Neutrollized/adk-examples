import os
import json
import vertexai
from vertexai import agent_engines
from google.adk.sessions import VertexAiSessionService


#--------------------
# config
#--------------------
project_id = os.getenv('GOOGLE_CLOUD_PROJECT')
location = os.getenv('GOOGLE_CLOUD_LOCATION')
reasoning_engine_resource_id = "7328790356894416896"    # UPDATE ME
reasoning_engine_name = f"projects/{project_id}/locations/{location}/reasoningEngines/{reasoning_engine_resource_id}"

adk_app = agent_engines.get(reasoning_engine_name)
#print(adk_app.operation_schemas())

session_service = VertexAiSessionService(project="gcp-demos-390500", location="us-central1")

#user_id = "user123"      # An identifier for the user
user_id = "user456"      # An identifier for the user


try:
    # Attempt to list sessions first
    listed_sessions_response = adk_app.list_sessions(user_id=user_id)
    # if there are no sessions for user
    if len(listed_sessions_response["sessions"]) != 0:
        #print(listed_sessions_response)
        print(f"> Existing session(s) found for {user_id}:")

        for id in listed_sessions_response["sessions"]:
            print(f"  - Session ID: {id["id"]}")

        # loading the first session
        print(f"> Loading session {listed_sessions_response["sessions"][0]["id"]}")
        session = adk_app.get_session(user_id=user_id, session_id=listed_sessions_response["sessions"][0]["id"])
    else:
        print(f"> No saved sessions found. Creating a new session for {user_id}...")
        if user_id == 'user456':
            session = adk_app.create_session(
                user_id=user_id,
                state={"units": "imperial"},
            )
        else:
            session = adk_app.create_session(user_id=user_id)
        print(f"> New session created with ID: {session["id"]}")

except Exception as e:
    print(f"An error occurred: {e}")


# weather_response is the output_key that is defined in the agent.py
print(f"USER: {session["userId"]}")
print(f"STATE: {session["state"]}")
