from fastapi import FastAPI, UploadFile, File, HTTPException
from uuid import uuid4
import shutil
import os
import requests

app = FastAPI()

@app.post("/ingest/upload")
async def upload_data(file: UploadFile = File(...)):
    ext = os.path.splitext(file.filename)[1]
    if ext not in [".txt", ".md", ".csv"]:
        raise HTTPException(status_code=400, detail="Unsupported file type")

    file_id = str(uuid4())
    save_path = f"uploads/{file_id}_{file.filename}"
    os.makedirs("uploads", exist_ok=True)
    with open(save_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    chunks = simulate_split_and_embed(save_path)

    for i, chunk in enumerate(chunks):
        try:
            requests.post("http://vector-memory-service:8004/vectors/upsert", json={
                "id": f"{file_id}_{i}",
                "vector": chunk["vector"],
                "metadata": {"source": file.filename, "chunk": i, "text": chunk["text"]}
            })
        except:
            pass

    return {"file_id": file_id, "chunks": len(chunks), "status": "processed"}

def simulate_split_and_embed(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        text = f.read()
    lines = text.strip().split("\n")
    chunks = []
    for line in lines:
        if line.strip():
            vector = [round(0.05 * i, 2) for i in range(10)]
            chunks.append({"text": line, "vector": vector})
    return chunks