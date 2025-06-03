from fastapi import FastAPI, HTTPException
from queue import enqueue, processed_jobs
from uuid import uuid4

app = FastAPI()

@app.post("/enqueue/fine-tune")
def enqueue_fine_tune(model_id: str):
    job_id = str(uuid4())
    job = {"job_id": job_id, "model_id": model_id}
    enqueue(job)
    return {"status": "queued", "job_id": job_id}

@app.get("/jobs/{job_id}")
def get_job(job_id: str):
    if job_id not in processed_jobs:
        raise HTTPException(status_code=404, detail="Job not found")
    return processed_jobs[job_id]