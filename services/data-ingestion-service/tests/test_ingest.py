from fastapi.testclient import TestClient
from main import app
import os

client = TestClient(app)

def test_upload_txt_file():
    os.makedirs("tests", exist_ok=True)
    with open("tests/sample.txt", "w") as f:
        f.write("Line one\nLine two\nLine three")
    with open("tests/sample.txt", "rb") as f:
        res = client.post("/ingest/upload", files={"file": ("sample.txt", f)})
        assert res.status_code == 200
        assert res.json()["chunks"] == 3