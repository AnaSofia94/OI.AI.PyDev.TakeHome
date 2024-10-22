from fastapi.testclient import TestClient
from src.batch import app

client = TestClient(app)


def test_upload_video():
    """Test uploading a valid video file through the API."""
    test_video_path = "english_Contest.mp4"  # Make sure this file exists

    with open(test_video_path, "rb") as f:
        response = client.post("/upload/", files={"file": f})
    assert response.status_code == 200
    response_data = response.json()
    assert "compressed_size" in response_data
    assert "original_size" in response_data
    assert "compression_ratio" in response_data