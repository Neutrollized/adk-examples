#! /bin/sh

AE_PROJECT="[PROJECT_ID_HERE]"  # UPDATE ME!
AE_LOCATION="us-central1"
AE_RESOURCE_ID="[AGENT_ID_HERE]"      # UPDATE ME!


curl \
-H "Authorization: Bearer $(gcloud auth print-access-token)" \
-H "Content-Type: application/json" \
  https://${AE_LOCATION}-aiplatform.googleapis.com/v1/projects/${AE_PROJECT}/locations/${AE_LOCATION}/reasoningEngines/${AE_RESOURCE_ID}:streamQuery?alt=sse -d '{
  "class_method": "stream_query",
  "input": {
    "user_id": "user123",
    "session_id": "[AE_SESSION_ID_HERE]",
    "message": "What is the weather in Valencia, Spain?",
  } 
}'
