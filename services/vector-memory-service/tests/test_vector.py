from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_upsert_and_query():
    v = [0.1 * i for i in range(10)]
    res = client.post("/vectors/upsert", json={"id": "vec1", "vector": v, "metadata": {"label": "test"}})
    assert res.status_code == 200

    q = {"vector": v, "top_k": 1}
    res2 = client.post("/vectors/query", json=q)
    assert res2.status_code == 200
    assert res2.json()[0]["id"] == "vec1"