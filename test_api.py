import pytest
from fastapi.testclient import TestClient
from main import app  # Import your FastAPI app
from routes.game_routes import game_routes
from routes.leaderboard_routes import leaderboard_routes


client = TestClient(app)

# ✅ Test GET Leaderboard
def test_get_leaderboard():
    response = client.get("/leaderboard")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)
    assert "leaderboard" in response.json()

# ✅ Test POST Add Score
def test_post_leaderboard_entry():
    payload = {"player_name": "TestPlayer", "score": 50}
    response = client.post("/leaderboard", json=payload)
    assert response.status_code == 200
    assert response.json()["message"] == "Score added successfully!"

# ✅ Test Start Game (GET /start)
def test_get_start():
    response = client.get("/start")
    assert response.status_code == 200
    assert "start_word" in response.json()
    assert "finish_word" in response.json()

# ✅ Test Fetch Similar Words
def test_get_similar_words():
    response = client.get("/similar/apple")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)
    assert "similar_words" in response.json()
