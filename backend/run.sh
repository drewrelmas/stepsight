#!/bin/bash

# StepSight Development Server Start Script
# 
# Configure data path using environment variable:
#    export STEPSIGHT_DATA_PATH="/path/to/your/data"
#    ./run.sh

echo "Starting StepSight API Development Server..."

# Show which data path will be used
if [ -n "$STEPSIGHT_DATA_PATH" ]; then
    echo "Using data path from environment: $STEPSIGHT_DATA_PATH"
else
    echo "Need to set STEPSIGHT_DATA_PATH environment variable to point to your data directory"
    exit 1
fi

python3 -m uvicorn main:app --reload --host 0.0.0.0 --port 8000