import os
import json
from google import auth as google_auth
from google.auth.transport import requests as google_requests
import requests


#----------------------------------
# config
#----------------------------------
project_id = os.getenv('GOOGLE_CLOUD_PROJECT')
location = os.getenv('GOOGLE_CLOUD_LOCATION')
reasoning_engine_resource_id = "7328790356894416896"    # UPDATE ME!
user_id = "user456"
session_id = "5287404633172475904"                      # UPDATE ME!


#------------------------
# helper
#------------------------
def get_identity_token():
    credentials, _ = google_auth.default()
    auth_request = google_requests.Request()
    credentials.refresh(auth_request)
    return credentials.token


# https://cloud.google.com/vertex-ai/generative-ai/docs/agent-engine/use/adk#requests_3
response = requests.post(
    f"https://{location}-aiplatform.googleapis.com/v1/projects/{project_id}/locations/{location}/reasoningEngines/{reasoning_engine_resource_id}:streamQuery",
    headers={
        "Content-Type": "application/json",
        "Authorization": f"Bearer {get_identity_token()}",
    },
    data=json.dumps({
        "class_method": "stream_query",
        "input": {
            "user_id": user_id,
            "session_id": session_id,
            "message": "What is the weather in san jose, usa?",
        },
    }),
    stream=False,
)

print(response.text)
