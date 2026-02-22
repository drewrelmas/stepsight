# StepSight - Barebones

An ultra-minimal fitness data explorer stripped down to essentials.

## Quick Start

### Prerequisites
- Python 3.7+ (for backend)
- Node.js 14+ (for frontend)

### Installation & Setup

1. **Set up Python virtual environment for backend:**
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

2. **Install frontend dependencies:**
```bash
cd frontend
npm install
```

> **Important**: Always activate the virtual environment (`source venv/bin/activate`) before running the backend server.

### Running the Application

You'll need to run both the backend and frontend in separate terminals:

#### Terminal 1 - Start the Backend (API Server)
```bash
cd backend
source venv/bin/activate  # Activate virtual environment

# Set the data path to your Strava export
export STEPSIGHT_DATA_PATH="/path/to/your/data/export_28658334"

# Option 1: Use the run script
./run.sh

# Option 2: Run uvicorn directly  
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```
The API will be available at: http://localhost:8000

#### Terminal 2 - Start the Frontend (React App)
```bash
cd frontend
npm start
```
The frontend will be available at: http://localhost:3000

The React app will automatically connect to the FastAPI backend. Visit http://localhost:3000 to see your activities displayed as raw data with minimal styling.