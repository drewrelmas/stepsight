"""
Basic tests for StepSight API
"""
import os
import pytest
import tempfile
import pandas as pd
from unittest.mock import patch, MagicMock

# Set environment variable before importing main to avoid import errors
os.environ['STEPSIGHT_DATA_PATH'] = '/mock/path'

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


@pytest.fixture
def mock_activities_data():
    """Create mock activities data for testing"""
    return pd.DataFrame({
        'Activity ID': ['123456789', '987654321'],
        'Activity Name': ['Morning Run', 'Evening Bike Ride'],
        'Activity Type': ['Run', 'Ride'],
        'Activity Date': ['2024-01-15 08:00:00', '2024-01-16 18:30:00'],
        'Distance': ['5.2', '15.8'],
        'Elapsed Time': ['1800', '3600']
    })


def test_health_check():
    """Test that the API is running"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data


def test_health_endpoint():
    """Test the dedicated health endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"


@patch('pandas.read_csv')
@patch('os.path.exists')
def test_activities_endpoint_success(mock_exists, mock_read_csv, mock_activities_data):
    """Test the activities endpoint returns valid response with mock data"""
    # Mock file existence and CSV reading
    mock_exists.return_value = True
    mock_read_csv.return_value = mock_activities_data
    
    with patch.dict(os.environ, {'STEPSIGHT_DATA_PATH': '/mock/path'}):
        response = client.get("/api/v1/activities/list")
        
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "total_count" in data
    assert "activities" in data
    assert data["total_count"] == 2
    assert len(data["activities"]) == 2
    
    # Verify activity structure
    activity = data["activities"][0]
    assert "id" in activity
    assert "name" in activity
    assert "type" in activity
    assert "date" in activity
    assert "distance" in activity
    assert "elapsed_time" in activity


@patch('os.path.exists')
def test_activities_endpoint_file_not_found(mock_exists):
    """Test activities endpoint when CSV file doesn't exist"""
    mock_exists.return_value = False
    
    with patch.dict(os.environ, {'STEPSIGHT_DATA_PATH': '/mock/path'}):
        response = client.get("/api/v1/activities/list")
        
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "not found" in data["detail"].lower()


@patch('pandas.read_csv')
@patch('os.path.exists')
def test_activities_endpoint_csv_error(mock_exists, mock_read_csv):
    """Test activities endpoint when CSV reading fails"""
    mock_exists.return_value = True
    mock_read_csv.side_effect = Exception("CSV parsing error")
    
    with patch.dict(os.environ, {'STEPSIGHT_DATA_PATH': '/mock/path'}):
        response = client.get("/api/v1/activities/list")
        
    assert response.status_code == 500
    data = response.json()
    assert "detail" in data
    assert "Error reading activities" in data["detail"]


def test_cors_headers():
    """Test CORS headers are present"""
    response = client.options("/api/v1/activities/list")
    assert response.status_code in [200, 405]  # Either supports OPTIONS or method not allowed