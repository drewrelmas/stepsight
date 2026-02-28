#!/bin/bash

# StepSight Development Server Start Script
# 
# Configure data path using environment variable:
#    export STEPSIGHT_DATA_PATH="/path/to/your/data"
#    ./run.sh

echo "Starting StepSight API Development Server..."

# Ensure the backend's virtual environment is active
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_ACTIVATE="$SCRIPT_DIR/venv/bin/activate"
if [ -f "$VENV_ACTIVATE" ]; then
    # shellcheck source=/dev/null
    source "$VENV_ACTIVATE"
else
    echo "Backend virtual environment not found. Run 'python3 -m venv venv' inside backend/ first."
    exit 0
fi

ENV_FILE="$SCRIPT_DIR/../.env"
if [ -f "$ENV_FILE" ]; then
    set -a
    # shellcheck source=/dev/null
    source "$ENV_FILE"
    set +a
    echo "Loaded environment variables from $ENV_FILE"
fi

# Show which data path will be used
if [ -n "$STEPSIGHT_DATA_PATH" ]; then
    echo "Using data path from environment: $STEPSIGHT_DATA_PATH"
else
    echo "Need to set STEPSIGHT_DATA_PATH environment variable to point to your data directory"
    exit 0
fi

PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
export PYTHONPATH="$PROJECT_ROOT${PYTHONPATH:+:$PYTHONPATH}"

echo "Python path configured for backend package: $PROJECT_ROOT"

pushd "$PROJECT_ROOT" >/dev/null || exit 1
python -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
popd >/dev/null