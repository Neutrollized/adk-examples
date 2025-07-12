#! /bin/sh

PROJECT_ID="[PROJECT_ID_HERE]"  # UPDATE ME!
LOCATION="us-central1"
AGENT_ID="[AGENT_ID_HERE]"      # UPDATE ME!


curl \
-H "Authorization: Bearer $(gcloud auth print-access-token)" \
-H "Content-Type: application/json" \
  https://${LOCATION}-aiplatform.googleapis.com/v1/projects/${PROJECT_ID}/locations/${LOCATION}/reasoningEngines/${AGENT_ID}:streamQuery?alt=sse -d '{
  "class_method": "stream_query",
  "input": {
    "user_id": "user123",
    "session_id": "[SESSION_ID_HERE]",
    "message": "What is the weather in Valencia, Spain?",
  } 
}'
