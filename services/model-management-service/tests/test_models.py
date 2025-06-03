from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_model_upload_and_list():
    with open("tests/sample-model.bin", "wb") as f:
        f.write(b"dummy-model")
    with open("tests/sample-model.bin", "rb") as f:
        res = client.post("/models/upload", files={"file": ("sample-model.bin", f)})
        assert res.status_code == 200
        data = res.json()
        assert "id" in data

    res = client.get("/models")
    assert res.status_code == 200
    assert isinstance(res.json(), list)