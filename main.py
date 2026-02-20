import os
import uuid
import time
import threading
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict

# Initialize app
app = FastAPI()

# Allow all frontend domains (adjust later if you want stricter)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Store jobs in-memory (fake processing)
jobs: Dict[str, Dict] = {}

# Request schema
class ProcessRequest(BaseModel):
    video_url: str
    openai_key: str
    settings: dict

# Fake AI processing function
def fake_ai_processing(job_id: str):
    time.sleep(5)  # simulate processing delay
    jobs[job_id]["status"] = "completed"
    jobs[job_id]["clips"] = [
        {
            "clip_url": "https://samplelib.com/lib/preview/mp4/sample-5s.mp4",
            "duration": 30,
            "viral_score": 8.7
        }
    ]

# Root route
@app.get("/")
def root():
    return {"status": "Backend running"}

# Start processing a video
@app.post("/process")
def process_video(request: ProcessRequest):
    job_id = str(uuid.uuid4())
    jobs[job_id] = {"status": "processing", "clips": []}
    thread = threading.Thread(target=fake_ai_processing, args=(job_id,))
    thread.start()
    return {"job_id": job_id}

# Check job status
@app.get("/status/{job_id}")
def check_status(job_id: str):
    if job_id not in jobs:
        return {"error": "Job not found"}
    return jobs[job_id]

# This is critical for Railway
if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.environ.get("PORT", 8000))  # <- Railway will provide PORT
    uvicorn.run("main:app", host="0.0.0.0", port=port)
