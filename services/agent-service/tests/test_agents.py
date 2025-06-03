from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_agent_create_and_respond():
    res = client.post("/agents/create", json={"name": "Lingra", "goal": "Answer questions"})
    assert res.status_code == 200
    agent_id = res.json()["agent_id"]

    res2 = client.post("/agents/message", json={"agent_id": agent_id, "message": "Hello"})
    assert res2.status_code == 200
    assert "response" in res2.json()