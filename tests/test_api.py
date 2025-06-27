import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from fastapi.testclient import TestClient
from main import app  # Import your FastAPI app
import pytest

# Use a TestClient for making requests to the FastAPI app
client = TestClient(app)

# Define a valid API key for testing, matching the one in main.py
VALID_API_KEY = "AdityaSalagare"
HEADERS = {"X-API-Key": VALID_API_KEY}

def test_read_root():
    """
    Test that the root endpoint is accessible and returns a welcome message.
    """
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the Biztel AI Analysis API!"}

def test_get_summary_unauthorized():
    """
    Test that the /summary endpoint returns a 401 Unauthorized error
    when no API key is provided.
    """
    # Note: The test client will raise an exception if the header is missing,
    # so we expect a 422 Unprocessable Entity error instead of 401 for a missing header.
    # A 401 would be returned for an invalid key.
    response = client.get("/summary", headers={"X-API-Key": "invalid-key"})
    assert response.status_code == 401

def test_get_summary_authorized():
    """
    Test that the /summary endpoint returns a successful response
    with a valid API key.
    """
    # This test assumes the data file exists.
    if os.path.exists('BiztelAI_DS_Dataset_V1.json'):
        response = client.get("/summary", headers=HEADERS)
        assert response.status_code == 200
        data = response.json()
        assert "total_transcripts" in data
        assert "total_messages" in data
    else:
        pytest.skip("Skipping summary test because data file is not found.")

def test_transform_text_authorized():
    """
    Test the /transform endpoint with a valid API key.
    """
    response = client.post(
        "/transform",
        headers=HEADERS,
        json={"text": "This is a test sentence."}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["original_text"] == "This is a test sentence."
    assert "processed_text" in data 