from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_enqueue_job():
    res = client.post("/enqueue/fine-tune", params={"model_id": "test-123"})
    assert res.status_code == 200
    job_id = res.json()["job_id"]

    res2 = client.get(f"/jobs/{job_id}")
    assert res2.status_code in [200, 404]