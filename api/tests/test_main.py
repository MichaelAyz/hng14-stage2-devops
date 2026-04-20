import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from main import app

client = TestClient(app)

@pytest.fixture
def mock_redis():
    with patch('main.r') as mock:
        yield mock

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "API is running"}

def test_create_job(mock_redis):
    response = client.post("/jobs")
    assert response.status_code == 200
    data = response.json()
    assert "job_id" in data
    
    mock_redis.lpush.assert_called_once()
    mock_redis.hset.assert_called_once()

def test_get_job_found(mock_redis):
    mock_redis.hget.return_value = b"completed"
    
    job_id = "test-job-123"
    response = client.get(f"/jobs/{job_id}")
    
    assert response.status_code == 200
    data = response.json()
    assert data["job_id"] == job_id
    assert data["status"] == "completed"

def test_get_job_not_found(mock_redis):
    mock_redis.hget.return_value = None
    
    job_id = "missing-job-123"
    response = client.get(f"/jobs/{job_id}")
    
    assert response.status_code == 200
    assert response.json() == {"error": "not found"}
