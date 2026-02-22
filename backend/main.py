import os
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import activities

logger = logging.getLogger("uvicorn.app")

DATA_PATH = os.getenv('STEPSIGHT_DATA_PATH')
if not DATA_PATH:
    logger.error("STEPSIGHT_DATA_PATH environment variable is required but not set")
    raise ValueError("STEPSIGHT_DATA_PATH environment variable is required but not set")

app = FastAPI(title="StepSight API", description="Fitness data analysis API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(activities.router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "StepSight API is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}