#! /bin/sh

if [ -f .env ]; then
    export $(echo $(grep -v '^#' .env | xargs))
fi


curl \
-H "Authorization: Bearer $(gcloud auth print-access-token)" \
-H "Content-Type: application/json" \
  https://${AE_LOCATION}-aiplatform.googleapis.com/v1/projects/${AE_PROJECT}/locations/${AE_LOCATION}/reasoningEngines/${AE_RESOURCE_ID}:streamQuery?alt=sse -d '{
  "class_method": "stream_query",
  "input": {
    "user_id": "user456",
    "session_id": "'"${AE_SESSION_ID}"'",
    "message": "What is the weather in Valencia, Spain?",
  } 
}'
