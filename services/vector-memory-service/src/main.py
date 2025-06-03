from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import numpy as np
from uuid import uuid4

app = FastAPI()
vector_store = {}

class VectorItem(BaseModel):
    id: str
    vector: List[float]
    metadata: dict

class QueryVector(BaseModel):
    vector: List[float]
    top_k: int = 3

@app.post("/vectors/upsert")
def upsert_vector(item: VectorItem):
    vector_store[item.id] = {
        "vector": np.array(item.vector),
        "metadata": item.metadata
    }
    return {"status": "stored", "id": item.id}

@app.post("/vectors/query")
def query_vector(query: QueryVector):
    if not vector_store:
        raise HTTPException(status_code=404, detail="No vectors available")

    query_vec = np.array(query.vector)
    similarities = []
    for item_id, data in vector_store.items():
        sim = cosine_similarity(query_vec, data["vector"])
        similarities.append((item_id, sim, data["metadata"]))

    similarities.sort(key=lambda x: x[1], reverse=True)
    top_results = similarities[:query.top_k]
    return [{"id": x[0], "score": float(x[1]), "metadata": x[2]} for x in top_results]

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))