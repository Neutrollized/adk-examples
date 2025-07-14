import os
import json
from google import auth as google_auth
from google.auth.transport import requests as google_requests
import requests


#----------------------------------
# config
#----------------------------------
project_id = os.getenv('AE_PROJECT')
location = os.getenv('AE_LOCATION')
reasoning_engine_resource_id = os.getenv('AE_RESOURCE_ID')
session_id = os.getenv('AE_SESSION_ID')
user_id = "user456"


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
            "message": "What is the weather in San Jose, USA?",
        },
    }),
    stream=False,
)

print(response.text)
