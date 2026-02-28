from fastapi import APIRouter, HTTPException
import os
import logging
import pandas as pd
from ..models.activity import Activity

# Use uvicorn's logger for consistency
logger = logging.getLogger("uvicorn.app")

router = APIRouter(prefix="/activities", tags=["activities"])

# Get data path from environment variable (required)
DATA_PATH = os.getenv('STEPSIGHT_DATA_PATH')
if not DATA_PATH:
    logger.error("STEPSIGHT_DATA_PATH environment variable is required but not set")
    raise ValueError("STEPSIGHT_DATA_PATH environment variable is required but not set")
logger.info(f"Activities module using data path: {DATA_PATH}")

@router.get("/list")
async def list_activities():
    """List all activities from the CSV file"""
    try:
        csv_path = os.path.join(DATA_PATH, "activities.csv")
        
        if not os.path.exists(csv_path):
            raise HTTPException(status_code=404, detail="Activities file not found at path: " + csv_path)
        
        df = pd.read_csv(csv_path)
        
        activities = []
        for _, row in df.iterrows():
            activity = {
                "id": str(row["Activity ID"]),
                "name": str(row["Activity Name"]),
                "type": str(row["Activity Type"]),
                "date": str(row["Activity Date"]),
                "distance": float(str(row["Distance"]).replace(',', '')) if pd.notna(row["Distance"]) else None,
                "elapsed_time": int(str(row["Elapsed Time"]).replace(',', '')) if pd.notna(row["Elapsed Time"]) else None,
            }
            activities.append(activity)
        
        return {
            "total_count": len(activities),
            "activities": activities
        }
    except HTTPException:
        # Re-raise HTTPExceptions (like 404) as-is
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading activities: {str(e)}")

@router.get("/{activity_id}")
async def get_activity(activity_id: str):
    """Get a single activity by ID"""
    try:
        csv_path = os.path.join(DATA_PATH, "activities.csv")
        df = pd.read_csv(csv_path)
        
        activity_row = df[df["Activity ID"] == int(activity_id)]
        if activity_row.empty:
            raise HTTPException(status_code=404, detail="Activity not found")
        
        row = activity_row.iloc[0]
        activity = {
            "id": str(row["Activity ID"]),
            "name": str(row["Activity Name"]),
            "type": str(row["Activity Type"]),
            "date": str(row["Activity Date"]),
            "distance": float(str(row["Distance"]).replace(',', '')) if pd.notna(row["Distance"]) else None,
            "elapsed_time": int(str(row["Elapsed Time"]).replace(',', '')) if pd.notna(row["Elapsed Time"]) else None,
        }
        
        return activity
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting activity: {str(e)}")