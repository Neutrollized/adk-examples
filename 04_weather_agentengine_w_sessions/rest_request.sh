#! /bin/sh

GOOGLE_CLOUD_PROJECT="[PROJECT_ID_HERE]"  # UPDATE ME!
GOOGLE_CLOUD_LOCATION="us-central1"
GOOGLE_CLOUD_AGENT_ENGINE_ID="[AGENT_ID_HERE]"      # UPDATE ME!


curl \
-H "Authorization: Bearer $(gcloud auth print-access-token)" \
-H "Content-Type: application/json" \
  https://${GOOGLE_CLOUD_LOCATION}-aiplatform.googleapis.com/v1/projects/${GOOGLE_CLOUD_PROJECT}/locations/${GOOGLE_CLOUD_LOCATION}/reasoningEngines/${GOOGLE_CLOUD_AGENT_ENGINE_ID}:streamQuery?alt=sse -d '{
  "class_method": "stream_query",
  "input": {
    "user_id": "user123",
    "session_id": "[SESSION_ID_HERE]",
    "message": "What is the weather in Valencia, Spain?",
  } 
}'
