from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_valid_progress():
    payload = {
        "user_id": "khushi",
        "video_id": "yt123",
        "start_time": 10,
        "end_time": 30,
        "watched_time": 20
    }
    response = client.post("/save_progress", json=payload)
    assert response.status_code == 200

def test_invalid_interval():
    payload = {
        "user_id": "khushi",
        "video_id": "yt123",
        "start_time": 50,
        "end_time": 20,
        "watched_time": 30
    }
    response = client.post("/save_progress", json=payload)
    assert response.status_code == 400

def test_get_progress():
    response = client.get("/get_progress/khushi/yt123")
    assert response.status_code == 200
    assert "watched_intervals" in response.json()
