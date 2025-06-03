import time
import threading
from uuid import uuid4

queue = []
processed_jobs = {}

def enqueue(job):
    queue.append(job)

def worker():
    print("[WORKER] Started")
    while True:
        if queue:
            job = queue.pop(0)
            job_id = job["job_id"]
            print(f"[WORKER] Processing job: {job_id}")
            processed_jobs[job_id] = {**job, "status": "processing"}
            time.sleep(3)
            processed_jobs[job_id]["status"] = "completed"
            print(f"[WORKER] Completed job: {job_id}")
        else:
            time.sleep(1)

threading.Thread(target=worker, daemon=True).start()