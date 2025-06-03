from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import os, shutil
from uuid import uuid4

app = FastAPI()

models_db = {}
fine_tune_queue = []

@app.post("/models/upload")
async def upload_model(file: UploadFile = File(...)):
    ext = os.path.splitext(file.filename)[1]
    if ext not in [".pt", ".bin", ".gguf"]:
        raise HTTPException(status_code=400, detail="Unsupported model format")

    model_id = str(uuid4())
    os.makedirs("model_repository", exist_ok=True)
    save_path = f"model_repository/{model_id}{ext}"
    with open(save_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    models_db[model_id] = {
        "id": model_id,
        "filename": file.filename,
        "path": save_path,
        "status": "uploaded"
    }

    return {"id": model_id, "message": "Model uploaded"}

@app.get("/models")
def list_models():
    return list(models_db.values())

@app.post("/models/{model_id}/trigger-finetune")
def trigger_finetune(model_id: str):
    if model_id not in models_db:
        raise HTTPException(status_code=404, detail="Model not found")

    job_id = str(uuid4())
    fine_tune_queue.append({
        "job_id": job_id,
        "model_id": model_id,
        "status": "queued"
    })

    print(f"[QUEUE] New fine-tune job: {job_id} for model: {model_id}")
    return {"job_id": job_id, "status": "queued"}