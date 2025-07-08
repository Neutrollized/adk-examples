# Dockerfile
FROM python:3.12-slim

# Set environment variables
ENV PYTHONUNBUFFERED=True
ENV APP_HOME="/app"

WORKDIR $APP_HOME

# Copy requirements.txt and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy your application code
COPY . .

# Command to run your FastAPI application with Uvicorn
CMD ["fastmcp", "run", "./server.py", "--transport", "sse"]
